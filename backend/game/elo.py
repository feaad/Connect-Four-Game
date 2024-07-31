from core.dataclasses import GameResult
from core.models import Player


class EloRating:
    """
    The Elo rating system is a method for calculating the relative skill levels
    of players in two-player games.

    """

    K = 32  # K-factor can be adjusted

    @staticmethod
    def expected_score(player_a: Player, player_b: Player) -> float:
        """
        Calculate the expected score for player_a against player_b.

        Parameters
        ----------
        player_a : Player
            The first player in the game.

        player_b : Player
            The second player in the game.

        Returns
        -------
        float
            The expected score for player_a against player_b.

        """
        return 1 / (1 + 10 ** ((player_b.elo - player_a.elo) / 400))

    @staticmethod
    def update_rating(
        current_elo: int, expected_score: float, actual_score: float
    ) -> int:
        """
        Update the Elo rating based on the actual game result.

        Parameters
        ----------
        current_elo : int
            The current Elo rating of the player.

        expected_score : float
            The expected score of the player.

        actual_score : float
            The actual score of the player.

        Returns
        -------
        int
            The updated Elo rating of the player.

        """
        rating = current_elo + EloRating.K * (actual_score - expected_score)

        return int(rating)

    @classmethod
    def update_player_elo(
        cls, player_one: Player, player_two: Player, result: GameResult
    ) -> None:
        """
        Update the Elo ratings for both players after a game.

        Parameters
        ----------
        player_one : Player
            The first player in the game.

        player_two : Player
            The second player in the game.

        result : GameResult
            The result of the game (WIN, LOSS, or DRAW).

        """
        actual_score_a = result.value
        actual_score_b = 1 - actual_score_a

        expected_score_b = cls.expected_score(player_two, player_one)
        expected_score_a = cls.expected_score(player_one, player_two)

        player_one.elo = cls.update_rating(
            player_one.elo, expected_score_a, actual_score_a
        )
        player_two.elo = cls.update_rating(
            player_two.elo, expected_score_b, actual_score_b
        )

    # TODO: Implement Elo rating history
