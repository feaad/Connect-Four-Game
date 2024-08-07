from random import sample
from uuid import UUID

import game.utils as utils
from core.constants import (
    BACKENDS,
    CONNECT,
    DEFAULT_COLUMNS,
    DEFAULT_ROWS,
    DIFFICULTY_LEVELS,
)
from core.dataclasses import Algorithm as cfa
from core.dataclasses import Status as cfs
from core.models import (
    PLAY_PREFERENCE_CHOICES,
    Algorithm,
    Game,
    GameInvitation,
    MatchMakingQueue,
    Move,
    Player,
    Status,
)
from core.utils import get_player, get_player_by_username
from django.db.models import Q
from game.match_making import add_player_to_queue, remove_player_from_queue
from game.mixins import PermissionMixin
from game.serializers import (
    CreateGameSerializer,
    CreateMoveSerializer,
    GameInvitationSerializer,
    GameSerializer,
    MatchMakingQueueSerializer,
    MatchmakingResponseSerializer,
    MoveSerializer,
)
from game.tasks import process_matchmaking
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

PLAY_PREFERENCE_KEYS = [choice[0] for choice in PLAY_PREFERENCE_CHOICES]


def error_response(message, code=status.HTTP_400_BAD_REQUEST):
    return Response({"error": message}, status=code)


class CreateGameView(PermissionMixin, GenericAPIView):
    serializer_class = CreateGameSerializer

    def _create_game(
        self,
        player,
        algorithm,
        rows,
        columns,
        difficulty_level,
        play_preference,
    ):
        ai_player = Player.objects.get(
            algorithm=Algorithm.objects.get(code_name=algorithm)
        )

        if play_preference == "first":
            player_one = player
            player_two = ai_player
        elif play_preference == "second":
            player_one = ai_player
            player_two = player
        else:
            player_one, player_two = sample([ai_player, ai_player], 2)

        game_data = {
            "player_one": player_one.player_id,
            "player_two": player_two.player_id,
            "rows": rows,
            "columns": columns,
            "difficulty_level": difficulty_level,
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
        return error_response(serializer.errors)

    def post(self, request: Request) -> Response:
        player = get_player(request.user)
        if not player:
            return error_response(
                "Not a valid user", status.HTTP_404_NOT_FOUND
            )

        try:
            rows = int(request.data.get("rows", DEFAULT_ROWS))
            columns = int(request.data.get("columns", DEFAULT_COLUMNS))
        except ValueError:
            return error_response("Column and Row must be integers")

        if rows < CONNECT or columns < CONNECT:
            return error_response(
                f"Rows and Columns must be at least {CONNECT}"
            )

        play_preference = request.data.get("play_preference", "random")

        if play_preference not in PLAY_PREFERENCE_KEYS:
            return error_response(f"Choose from {PLAY_PREFERENCE_KEYS}")

        try:
            difficulty_level = int(
                request.data.get("difficulty_level", DIFFICULTY_LEVELS["min"])
            )
        except ValueError:
            return error_response("Difficulty level must be an integer")

        if not (
            DIFFICULTY_LEVELS["min"]
            <= difficulty_level
            <= DIFFICULTY_LEVELS["max"]
        ):
            return error_response(
                f"Difficulty level must be between {DIFFICULTY_LEVELS['min']}"
                + f" and {DIFFICULTY_LEVELS['max']} inclusive"
            )

        algorithm = request.data.get("algorithm", str(cfa.RANDOM))

        if algorithm not in [alg.value for alg in cfa]:
            valid_options = ", ".join([alg.value for alg in cfa])
            return error_response(f"Choose from {valid_options}")

        return self._create_game(
            player, algorithm, rows, columns, difficulty_level, play_preference
        )


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
        "difficulty_level",
        "depth",
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
        "player_one__algorithm__code_name",
        "player_two__algorithm__code_name",
        "rows",
        "columns",
        "difficulty_level",
        "depth",
        "status__name",
        "current_turn__user__username",
        "current_turn__guest__username",
        "current_turn__algorithm__name",
        "current_turn__algorithm__code_name",
        "start_time",
        "end_time",
        "winner__user__username",
        "winner__guest__username",
        "winner__algorithm__name",
        "winner__algorithm__code_name",
        "created_by__user__username",
        "created_by__guest__username",
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
            status=Status.objects.get(name=cfs.QUEUED.value),
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


class GameInvitationViewSet(PermissionMixin, viewsets.ModelViewSet):
    serializer_class = GameInvitationSerializer
    http_method_names = ["get", "post"]
    queryset = GameInvitation.objects.all()
    filter_backends = BACKENDS

    filterset_fields = [
        "invitation_id",
        "sender",
        "receiver",
        "status",
        "game",
        "play_preference",
        "created_at",
    ]
    search_fields = [
        "sender__user__username",
        "sender__guest__username",
        "receiver__user__username",
        "receiver__guest__username",
        "status__name",
        "game",
        "play_preference",
        "created_at",
    ]
    ordering_fields = filterset_fields

    def get_queryset(self):
        """
        Return all games ordered by queue_id.

        """
        if player := get_player(self.request.user):
            return self.queryset.filter(
                Q(sender=player) | Q(receiver=player)
            ).order_by("created_at")
        else:
            return self.queryset.none()

    def create(self, request: Request) -> Response:
        sender = get_player(request.user)
        if not sender:
            return error_response(
                "Not a valid user", status.HTTP_404_NOT_FOUND
            )

        receiver = request.data.get("receiver")

        if not receiver:
            return error_response("Receiver are required.")

        receiver = get_player_by_username(receiver)

        if not receiver:
            return error_response(
                "Not a valid receiver", status.HTTP_404_NOT_FOUND
            )

        if receiver == sender:
            return error_response("You can't invite yourself.")

        try:
            rows = int(request.data.get("rows", DEFAULT_ROWS))
            columns = int(request.data.get("columns", DEFAULT_COLUMNS))
        except ValueError:
            return error_response("Column and Row must be integers")

        if rows < CONNECT or columns < CONNECT:
            return error_response(
                f"Rows and Columns must be at least {CONNECT}"
            )

        play_preference = request.data.get("play_preference", "random")

        if play_preference not in PLAY_PREFERENCE_KEYS:
            return error_response(f"Choose from {PLAY_PREFERENCE_KEYS}")

        invitation = GameInvitation.objects.create(
            sender=sender,
            receiver=receiver,
            play_preference=play_preference,
            rows=rows,
            columns=columns,
            status=Status.objects.get(name=cfs.PENDING.value),
        )
        # TODO: Send User Notification

        return Response(
            GameInvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def accept(self, request: Request, pk=None) -> Response:
        player = get_player(request.user)
        if not player:
            return error_response(
                "Not a valid user", status.HTTP_404_NOT_FOUND
            )

        try:
            invitation: GameInvitation = GameInvitation.objects.get(
                invitation_id=UUID(pk),
                status=Status.objects.get(name=cfs.PENDING.value),
            )
        except (ValueError, GameInvitation.DoesNotExist):
            return error_response(
                "Game Invitation does not exist",
                status.HTTP_404_NOT_FOUND,
            )

        if invitation.receiver != player:
            return error_response(
                "You are not the receiver of this invitation"
            )

        invitation.status = Status.objects.get(name=cfs.ACCEPTED.value)

        # Determine who plays first based on the sender's play preference
        if invitation.play_preference == "first":
            player_one = invitation.sender
            player_two = invitation.receiver
        elif invitation.play_preference == "second":
            player_one = invitation.receiver
            player_two = invitation.sender
        else:
            player_one, player_two = sample(
                [invitation.sender, invitation.receiver], 2
            )

        game_data = {
            "player_one": player_one.player_id,
            "player_two": player_two.player_id,
            "rows": invitation.rows,
            "columns": invitation.columns,
            "created_by": invitation.sender.player_id,
        }

        game_serializer = CreateGameSerializer(data=game_data)

        if not game_serializer.is_valid():
            return error_response(game_serializer.errors)

        game = game_serializer.save()

        invitation.game = game
        invitation.save()

        # TODO: Send User Notification

        return Response(
            GameInvitationSerializer(invitation).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request: Request, pk=None) -> Response:
        player = get_player(request.user)
        if not player:
            return error_response(
                "Not a valid user", status.HTTP_404_NOT_FOUND
            )

        try:
            invitation: GameInvitation = GameInvitation.objects.get(
                invitation_id=UUID(pk),
                status=Status.objects.get(name=cfs.PENDING.value),
            )
        except (ValueError, GameInvitation.DoesNotExist):
            return error_response(
                "Game Invitation does not exist",
                status.HTTP_404_NOT_FOUND,
            )

        if invitation.receiver != player:
            return error_response(
                "You are not the receiver of this invitation"
            )

        invitation.status = Status.objects.get(name=cfs.REJECTED.value)
        invitation.save()
        # TODO: Send User Notification

        return Response(
            GameInvitationSerializer(invitation).data,
            status=status.HTTP_200_OK,
        )


class MoveViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet for the Move model.
    """

    serializer_class = MoveSerializer
    queryset = Move.objects.all()
    http_method_names = ["get", "post"]
    filter_backends = BACKENDS

    filterset_fields = [
        "move_id",
        "game",
        "player",
        "column",
        "row",
        "is_undone",
    ]
    search_fields = [
        "move_id",
        "game__game_id",
        "player__user__username",
        "player__guest__username",
        "player__algorithm__name",
        "player__algorithm__code_name",
        "column",
        "row",
        "is_undone",
    ]
    ordering_fields = filterset_fields

    def get_queryset(self):
        """
        Return all games ordered by move_id.

        """
        if player := get_player(self.request.user):
            return self.queryset.filter(
                Q(player=player.player_id)
                | Q(game__player_one=player.player_id)
                | Q(game__player_two=player.player_id)
            ).order_by("updated_at")
        else:
            return self.queryset.none()

    def create(self, request: Request) -> Response:
        player = get_player(request.user)
        if not player:
            return error_response(
                "Not a valid user", status.HTTP_404_NOT_FOUND
            )

        game_id = request.data.get("game_id")

        try:
            column = int(request.data.get("column", -1))
            row = int(request.data.get("row", -1))
        except ValueError:
            return error_response("Column and Row must be integers")

        game = Game.objects.filter(game_id=game_id).first()

        if not game:
            return error_response(
                "Game does not exist", status.HTTP_404_NOT_FOUND
            )

        if game.player_one != player and game.player_two != player:
            return error_response(
                "You are not a player in this game",
            )

        if game.status.name not in [cfs.IN_PROGRESS.value, cfs.CREATED.value]:
            return error_response("Game is not in progress")

        if game.current_turn != player:
            return error_response("It is not your turn")

        if utils.is_board_full(game.board):
            return error_response("Board is full")

        if column < 0 or row < 0:
            return error_response("Column and Row are required")

        if column >= game.columns or row >= game.rows:
            return error_response(
                f"(Column,Row) must be less than ({game.columns},{game.rows})"
            )

        if not utils.is_valid_move(game.board, column, row):
            return error_response("Invalid move")

        move_data = {
            "game": game.game_id,
            "player": player.player_id,
            "column": column,
            "row": row,
        }

        serializer = CreateMoveSerializer(data=move_data)

        if serializer.is_valid():
            move = serializer.save()
            move_reponse = MoveSerializer(move)
            return Response(
                move_reponse.data,
                status=status.HTTP_201_CREATED,
            )

        return error_response(serializer.errors)

    @action(
        detail=False, methods=["post"], url_path="(?P<game_id>[^/.]+)/undo"
    )
    def undo(self, request: Request, game_id=None) -> Response:
        player = get_player(request.user)
        if not player:
            return error_response(
                "Not a valid user", status.HTTP_404_NOT_FOUND
            )

        try:
            move: Move = Move.objects.filter(
                game_id=UUID(game_id), player=player, is_undone=False
            ).latest("created_at")
        except (ValueError, Move.DoesNotExist):
            return error_response("No moves to undo")

        if not utils.can_undo_move(move):
            return error_response("You cannot undo this move")

        move.is_undone = True
        move.save()

        serializer = MoveSerializer(move)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
