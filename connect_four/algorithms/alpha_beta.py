from connect_four.board.colour import Colour

from .algorithm import Algorithm


class AlphaBeta(Algorithm):
    
    def __init__(self, colour: Colour) -> None:
        super().__init__(colour)