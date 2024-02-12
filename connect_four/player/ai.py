"""
File: ai.py
Project: Connect Four
File Created: Monday, 12th February 2024 10:27:21 AM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: Implementation of the AI Player
-----
Last Modified: Monday, 12th February 2024 10:47:05 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from random import choice
from typing import Optional

from algorithms.algorithm import Algorithm
from algorithms.algorithm_type import AlgorithmType
from algorithms.alpha_beta import AlphaBeta
from algorithms.min_max import MinMax

from connect_four.board.board import Board
from connect_four.board.colour import Colour

from .player import Player


class AI(Player):
    algo: Algorithm
    algo_type: AlgorithmType

    def __init__(
        self, name: str, colour: Colour, algo_type: AlgorithmType = AlgorithmType.RANDOM
    ) -> None:
        super().__init__(name, colour)
        self.algo_type = algo_type

        # TODO: Implement this
        if algo_type == AlgorithmType.MIN_MAX:
            self.algo = MinMax(colour)
        elif algo_type == AlgorithmType.ALPHA_BETA:
            self.algo = AlphaBeta(colour)
        else:
            self.algo = choice([MinMax(colour), AlphaBeta(colour)])

    def get_move(self, board: Optional[Board] = None) -> int:
        if board is None:
            raise ValueError("Board is None")

        if not self.is_turn:
            raise ValueError("It's not the {self.name}'s turn")
        
        return self.algo.get_best_move(board)
