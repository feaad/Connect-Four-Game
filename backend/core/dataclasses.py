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

    def __str__(self) -> str:
        return self.value


class Algorithm(Enum):
    """
    The algorithm used for ai.

    """

    MINIMAX = "Minimax"
    ALPHA_BETA = "Alpha Beta Pruning"
    MCTS = "Monte Carlo Tree Search"
    NN = "Neural Networks"
    RL = "Reinforcement Learning"
    RANDOM = "Random"

    def __str__(self) -> str:
        if self == Algorithm.RANDOM:
            choices = [
                alg.value for alg in Algorithm if alg != Algorithm.RANDOM
            ]
            return choice(choices)
        return self.value
