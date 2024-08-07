from core import models
from core.constants import DEFAULT_COLUMNS, DEFAULT_ROWS, EMPTY
from core.dataclasses import Status as cfs
from core.utils import get_username_or_name
from game.utils import compute_depth
from rest_framework import serializers


class CreateGameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Create Game Object
    """

    class Meta:
        """
        Meta class for the CreateGameSerializer
        """

        model = models.Game
        fields = [
            "game_id",
            "player_one",
            "player_two",
            "rows",
            "columns",
            "difficulty_level",
            "created_by",
        ]
        read_only_fields = ["game_id"]

    def create(self, validated_data):
        """
        Create a new game instance with an initialized board.
        """
        rows = validated_data.get("rows", DEFAULT_ROWS)
        columns = validated_data.get("columns", DEFAULT_COLUMNS)
        board = [[EMPTY for _ in range(columns)] for _ in range(rows)]
        validated_data["board"] = board
        validated_data["status"] = models.Status.objects.get(name=cfs.CREATED)
        validated_data["current_turn"] = validated_data["player_one"]

        if validated_data.get("difficulty_level"):
            if depth := compute_depth(
                validated_data["difficulty_level"],
                validated_data["player_one"],
                validated_data["player_two"],
            ):
                validated_data["depth"] = depth

        return super().create(validated_data)


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game Object

    """

    player_one_username = serializers.SerializerMethodField()
    player_two_username = serializers.SerializerMethodField()
    current_turn_username = serializers.SerializerMethodField()
    winner_username = serializers.SerializerMethodField()
    created_by_username = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the GameSerializer

        """

        model = models.Game
        fields = [
            "game_id",
            "player_one_username",
            "player_two_username",
            "rows",
            "columns",
            "board",
            "difficulty_level",
            "depth",
            "status_name",
            "current_turn_username",
            "start_time",
            "end_time",
            "winner_username",
            "created_by_username",
            "created_at",
        ]
        read_only_fields = ["game_id"]

    def get_player_one_username(self, obj: models.Game) -> str:
        """
        Get the username of player one
        """
        return get_username_or_name(obj.player_one)

    def get_player_two_username(self, obj: models.Game) -> str:
        """
        Get the username of player two
        """
        return get_username_or_name(obj.player_two)

    def get_current_turn_username(self, obj: models.Game) -> str:
        """
        Get the username of the current turn
        """
        return get_username_or_name(obj.current_turn)

    def get_winner_username(self, obj: models.Game) -> str:
        """
        Get the username of the winner
        """
        return get_username_or_name(obj.winner)

    def get_created_by_username(self, obj: models.Game) -> str:
        """
        Get the username of the creator
        """
        return get_username_or_name(obj.created_by)

    def get_status_name(self, obj: models.Game) -> str:
        """
        Get the name of the status
        """
        return obj.status.name if obj.status else None


class MatchMakingQueueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Match Making Object

    """

    status_name = serializers.SerializerMethodField()
    player_username = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the MatchMakingSerializer

        """

        model = models.MatchMakingQueue
        fields = [
            "queue_id",
            "player_username",
            "status_name",
            "game",
            "created_at",
        ]
        read_only_fields = ["queue_id", "player"]

    def get_status_name(self, obj: models.MatchMakingQueue) -> str:
        """
        Get the name of the status
        """
        return obj.status.name if obj.status else None

    def get_player_username(self, obj: models.MatchMakingQueue) -> str:
        """
        Get the username of the winner
        """
        return get_username_or_name(obj.player)


class MatchmakingResponseSerializer(serializers.Serializer):
    """
    Serializer for the Matchmaking Response
    """

    status = serializers.CharField()
    queue_id = serializers.UUIDField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class GameInvitationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game Invitation
    """

    sender_username = serializers.SerializerMethodField()
    receiver_username = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the GameInvitationSerializer

        """

        model = models.GameInvitation
        fields = [
            "invitation_id",
            "sender_username",
            "receiver_username",
            "status_name",
            "game",
            "play_preference",
            "rows",
            "columns",
            "created_at",
        ]
        read_only_fields = ["game_id"]

    def get_sender_username(self, obj: models.GameInvitation) -> str:
        """
        Get the username of the sender
        """
        return get_username_or_name(obj.sender)

    def get_receiver_username(self, obj: models.GameInvitation) -> str:
        """
        Get the username of the receiver
        """
        return get_username_or_name(obj.receiver)

    def get_status_name(self, obj: models.GameInvitation) -> str:
        """
        Get the name of the status
        """
        return obj.status.name if obj.status else None


class CreateMoveSerializer(serializers.ModelSerializer):
    """
    Serializer for the Move
    """

    class Meta:
        """
        Meta class for the MoveSerializer

        """

        model = models.Move
        fields = [
            "move_id",
            "game",
            "player",
            "column",
            "row",
            "is_undone",
        ]
        read_only_fields = ["move_id"]


class MoveSerializer(serializers.ModelSerializer):
    """
    Serializer for the Move
    """

    player_username = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the MoveSerializer

        """

        model = models.Move
        fields = [
            "move_id",
            "game",
            "player_username",
            "column",
            "row",
            "is_undone",
        ]
        read_only_fields = ["move_id"]

    def get_player_username(self, obj: models.Move) -> str:
        """
        Get the username of the player
        """
        return get_username_or_name(obj.player)
