from enum import Enum
from random import choice


class GameResult(Enum):
    """
    The result of a game.

    """

    WIN = 1
    DRAW = 0.5
    LOSS = 0


class Status(Enum):
    """
    The status of a match.

    """

    QUEUED = "Queued"
    MATCHED = "Matched"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    CREATED = "Created"
    ACCEPTED = "Accepted"
    PENDING = "Pending"
    REJECTED = "Rejected"
    P1W = "Player 1 Wins"
    P2W = "Player 2 Wins"
    DRAW = "Draw"

    def __str__(self) -> str:
        return self.value


class Algorithm(Enum):
    """
    The algorithm used for ai.

    """

    MINIMAX = "mystic"
    ALPHA_BETA = "sphinx"
    RANDOM = "Random"

    def __str__(self) -> str:
        if self == Algorithm.RANDOM:
            choices = [
                alg.value for alg in Algorithm if alg != Algorithm.RANDOM
            ]
            return choice(choices)
        return self.value

    def __eq__(self, other: object) -> bool:
        return (
            self.value == other.value
            if isinstance(other, Algorithm)
            else False
        )

    def __hash__(self) -> int:
        return hash(self.value)
