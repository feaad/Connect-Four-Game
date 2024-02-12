from algorithms.algorithm_type import AlgorithmType
from board.board import Board
from board.colour import Colour
from board.position import Position
from player.ai import AI
from player.human import Human

WIDTH = 7
HEIGHT = 6

dimensions = Position(WIDTH, HEIGHT)
board = Board(dim=dimensions)

human = Human("N", Colour.RED)
ai = AI("T", Colour.YELLOW, AlgorithmType.ALPHA_BETA)

is_human_turn = True


def switch_turn() -> None:
    global is_human_turn
    is_human_turn = not is_human_turn

    human.set_is_turn(is_human_turn)
    ai.set_is_turn(not is_human_turn)


def main():
    board.print_board()
    human.set_is_turn(is_human_turn)

    while not board.is_game_over():
        col = human.get_move()
        board.drop_token(col, human.get_colour())

        if board.is_game_over() == True:
            break

        switch_turn()

        col = ai.get_move(board)
        board.drop_token(col, ai.get_colour())

        switch_turn()

        board.print_board()

    board.print_board()


if __name__ == "__main__":
    main()
