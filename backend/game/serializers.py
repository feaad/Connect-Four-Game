from core import models
from rest_framework import serializers


def get_username_or_name(player: models.Player) -> str:
    """
    Helper method to get the username or name from a Player object.
    """
    if player is None:
        return None
    if player.user:
        return player.user.username
    elif player.guest:
        return player.guest.username
    elif player.algorithm:
        return player.algorithm.name
    return ""


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
            "board",
            "status",
            "current_turn",
            "start_time",
            "end_time",
            "winner",
            "created_by",
        ]
        read_only_fields = ["game_id"]


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
