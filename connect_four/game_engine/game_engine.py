from typing import Optional

from algorithms.algorithm_type import AlgorithmType
from board.board import Board
from board.colour import Colour
from board.position import Position
from player.ai import AI
from player.human import Human
from player.player import Player
from player.player_type import PlayerType

from .game_state import GameState


class GameEngine:
    player1: Optional[Player]
    player2: Optional[Player]

    is_player1_turn: bool

    game_state: GameState

    def __init__(self, width: int = 7, height: int = 6):
        dimensions = Position(width, height)
        self.board = Board(dim=dimensions)

        self.player1 = None
        self.player2 = None

        self.is_player1_turn = True
        self.game_state = GameState.SETUP

    def create_player(
        self,
        name: str,
        player_type: PlayerType,
        player1: bool = True,
        algorithm_type: Optional[AlgorithmType] = None,
    ):
        # TODO: Randomize which player goes first

        colour = Colour.RED if player1 else Colour.YELLOW

        if player_type == PlayerType.HUMAN:
            player = Human(name, colour)
        else:
            if algorithm_type is None:
                raise ValueError("Algorithm type must be provided for AI players")

            player = AI(name, colour, algorithm_type)

        if player1:
            self.player1 = player
        else:
            self.player2 = player
            self.game_state = GameState.PLAYING

    def switch_turn(self) -> None:
        self.is_player1_turn = not self.is_player1_turn

        self.player1.set_is_turn(self.is_player1_turn)
        self.player2.set_is_turn(not self.is_player1_turn)

    def play(self) -> None:
        if self.player1 is None or self.player2 is None:
            raise ValueError("Both players must be created before the game can start")

        self.board.print_board()
        self.player1.set_is_turn(self.is_player1_turn)

        # TODO: store state in database to allow for resuming games and
        # tracking game history as well as getting rid of the loop
        while not self.board.is_game_over():
            column = self.player1.get_move()
            self.board.drop_token(column, self.player1.get_colour())

            if self.board.is_game_over():
                if self.board.check_win():
                    self.game_state = GameState.PLAYER_1_WIN
                break

            self.switch_turn()

            column = self.player2.get_move(self.board)
            self.board.drop_token(column, self.player2.get_colour())

            if self.board.check_win():
                self.game_state = GameState.PLAYER_2_WIN
                break

            self.switch_turn()

            # TODO: remove this print statement
            print("🟡 AI, entereed the column number:", column + 1)
            self.board.print_board()

        if (
            self.game_state != GameState.PLAYER_1_WIN
            and self.game_state != GameState.PLAYER_2_WIN
        ):
            self.game_state = GameState.DRAW

        self.board.print_board()
        print(self.game_state)
