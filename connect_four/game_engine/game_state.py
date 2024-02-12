from enum import Enum


class GameState(Enum):

    """Defines the possible states of the game"""

    SETUP = 0
    PLAYING = 1
    DRAW = 2
    PLAYER_1_WIN = 3
    PLAYER_2_WIN = 4

    def __eq__(self, __value: object) -> bool:
        """
        The function checks if two objects of the GameState class are equal
        by comparing their values.

        Parameters
        ----------
        __value : object
            The "__value" parameter is an object that we are comparing to the
            current object for equality.

        Returns
        -------
            The `__eq__` method is returning `True` if the `__value` object is an
            instance of the `GameState` class and has the same `value`
            attribute as the current object (`self`). Otherwise, it returns
            `False`.

        """
        if isinstance(__value, GameState):
            return self.value == __value.value

        return False
