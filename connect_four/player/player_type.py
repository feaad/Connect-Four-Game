from enum import Enum


class PlayerType(Enum):
    """Defines the types of players that can play the game"""

    HUMAN = 0
    AI = 1

    def __eq__(self, other: object) -> bool:
        """
        The function checks if two objects of the PlayerType class are equal
        by comparing their values.

        Parameters
        ----------
        other : object
            The "other" parameter is an object that we are comparing to the
            current object for equality.

        Returns
        -------
            The `__eq__` method is returning `True` if the `other` object is an
            instance of the `PlayerType` class and has the same `value`
            attribute as the current object (`self`). Otherwise, it returns
            `False`.

        """
        if isinstance(other, PlayerType):
            return self.value == other.value

        return False
