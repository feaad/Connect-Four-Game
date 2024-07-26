from random import choice

from core.constants import (
    BACKENDS,
    CONNECT,
    DEFAULT_COLUMNS,
    DEFAULT_ROWS,
    EMPTY,
    PLAYER_ONE,
    PLAYER_TWO,
    RANDOM,
)
from core.models import Game, MatchMakingQueue, Status
from core.utils import get_player
from game.match_making import add_player_to_queue
from game.mixins import PermissionMixin
from game.serializers import (
    CreateGameSerializer,
    GameSerializer,
    MatchMakingQueueSerializer,
    MatchmakingResponseSerializer,
)
from game.tasks import process_matchmaking
from game.match_making import remove_player_from_queue
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class CreateGameView(PermissionMixin, GenericAPIView):
    serializer_class = CreateGameSerializer

    def _error_response(self, message, code=status.HTTP_400_BAD_REQUEST):
        return Response({"error": message}, status=code)

    def _create_game(self, player, rows, columns, turn):
        board = [[EMPTY for _ in range(columns)] for _ in range(rows)]
        player_one = player.player_id if turn == PLAYER_ONE else None
        player_two = player.player_id if turn == PLAYER_TWO else None
        current_turn = player_one if turn == PLAYER_ONE else player_two
        game_status = Status.objects.get(name="Created")
        game_data = {
            "player_one": player_one,
            "player_two": player_two,
            "rows": rows,
            "columns": columns,
            "board": board,
            "status": game_status.status_id,
            "current_turn": current_turn,
            "created_by": player.player_id,
        }
        serializer = self.get_serializer(data=game_data)
        if serializer.is_valid():
            game = serializer.save()
            game_reponse = GameSerializer(game)
            return Response(
                game_reponse.data,
                status=status.HTTP_201_CREATED,
            )
        return self._error_response(serializer.errors)

    def post(self, request: Request) -> Response:
        player = get_player(request.user)
        if not player:
            return self._error_response("Not a valid user")

        rows = int(request.data.get("rows", DEFAULT_ROWS))
        columns = int(request.data.get("columns", DEFAULT_COLUMNS))
        if rows < CONNECT or columns < CONNECT:
            return self._error_response(
                f"Rows and Columns must be at least {CONNECT}"
            )

        turn = int(request.data.get("turn", PLAYER_ONE))
        if turn not in [PLAYER_ONE, PLAYER_TWO, RANDOM]:
            return self._error_response(
                f"Choose from {PLAYER_ONE}, {PLAYER_TWO}, {RANDOM}"
            )

        if turn == RANDOM:
            turn = choice([PLAYER_ONE, PLAYER_TWO])

        return self._create_game(player, rows, columns, turn)


class GameViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Game model.
    """

    serializer_class = GameSerializer
    queryset = Game.objects.all()
    http_method_names = ["get"]
    filter_backends = BACKENDS

    filterset_fields = [
        "game_id",
        "player_one",
        "player_two",
        "rows",
        "columns",
        "status",
        "current_turn",
        "start_time",
        "end_time",
        "winner",
        "created_by",
    ]
    search_fields = [
        "game_id",
        "player_one__user__username",
        "player_two__user__username",
        "player_one__guest__username",
        "player_two__guest__username",
        "player_one__algorithm__name",
        "player_two__algorithm__name",
        "rows",
        "columns",
        "status__name",
        "current_turn__user__username",
        "current_turn__guest__username",
        "current_turn__algorithm__name",
        "start_time",
        "end_time",
        "winner__user__username",
        "winner__guest__username",
        "winner__algorithm__name",
        "created_by__user__username",
        "created_by__guest__username",
        "created_by__algorithm__name",
    ]
    ordering_fields = filterset_fields

    def get_queryset(self):
        """
        Return all games ordered by game_id.

        """
        return self.queryset.order_by("game_id")


class GameHistoryView(PermissionMixin, GenericAPIView):
    serializer_class = GameSerializer

    def get(self, request: Request) -> Response:
        player = get_player(request.user)
        if not player:
            return Response(
                {"error": "Player does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        games = Game.objects.filter(
            player_one=player.player_id
        ) | Game.objects.filter(player_two=player.player_id).order_by(
            "created_at"
        )
        game_serializer = GameSerializer(games, many=True)

        return Response(game_serializer.data, status=status.HTTP_200_OK)


class RequestMatchMakingView(PermissionMixin, GenericAPIView):
    """
    API endpoint to request a match making queue.
    """

    serializer_class = MatchmakingResponseSerializer

    def post(self, request: Request) -> Response:
        """
        Add the player to the matchmaking queue.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        player = get_player(request.user)
        if not player:
            return Response(
                {"error": "Player does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if player_matches := MatchMakingQueue.objects.filter(
            player=player.player_id,
            status=Status.objects.get(name="Queued"),
        ):
            response_data = {
                "status": "Player already in matchmaking queue",
                "queue_id": player_matches[0].queue_id,
            }
            serializer = MatchmakingResponseSerializer(response_data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        queue_id = add_player_to_queue(player.player_id, player.elo)

        # Optionally, trigger matchmaking immediately here
        process_matchmaking.apply_async()

        response_data = {
            "status": "Player added to matchmaking queue",
            "queue_id": queue_id,
        }
        serializer = MatchmakingResponseSerializer(response_data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CancelMatchMakingView(PermissionMixin, GenericAPIView):
    """
    API endpoint to cancel a match making queue.
    """

    def post(self, request: Request) -> Response:
        """
        Remove the player from the matchmaking queue.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        player = get_player(request.user)
        if not player:
            return Response(
                {"error": "Player does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        state = remove_player_from_queue(str(player.player_id))
        if state != 2:
            return Response(
                MatchmakingResponseSerializer(
                    {"status": "Match making not found"}
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_data = {
            "status": "Match making cancelled",
        }
        serializer = MatchmakingResponseSerializer(response_data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class GetMatchMakingQueueViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    API endpoint to get the match making queue.
    """

    serializer_class = MatchMakingQueueSerializer
    queryset = MatchMakingQueue.objects.all()
    http_method_names = ["get"]
    filter_backends = BACKENDS

    filterset_fields = ["status", "created_at"]
    search_fields = [
        "status__name",
        "created_at",
    ]
    ordering_fields = filterset_fields

    def get_queryset(self):
        """
        Return all games ordered by queue_id.

        """
        if player := get_player(self.request.user):
            return self.queryset.filter(player=player.player_id).order_by(
                "created_at"
            )
        else:
            return self.queryset.none()
