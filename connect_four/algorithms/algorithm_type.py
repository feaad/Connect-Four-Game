"""
File: algorithm_type.py
Project: Connect Four
File Created: Monday, 12th February 2024 10:50:51 AM
Author: feaad
Email: antwi-donkor_f@outlook.com
Version: 1.0
Brief: Implementation of the possible types of algorithm
-----
Last Modified: Monday, 12th February 2024 10:53:20 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from enum import Enum


class AlgorithmType(Enum):
    """Implementation of the possible types of algorithm"""

    RANDOM = 0
    MIN_MAX = 1
    ALPHA_BETA = 2

    def __eq__(self, other: object) -> bool:
        """
        The function checks if two objects of the AlgorithmType class are equal
        by comparing their values.

        Parameters
        ----------
        other : object
            The "other" parameter is an object that we are comparing to the
            current object for equality.

        Returns
        -------
            The `__eq__` method is returning `True` if the `other` object is an
            instance of the `AlgorithmType` class and has the same `value`
            attribute as the current object (`self`). Otherwise, it returns
            `False`.

        """
        if isinstance(other, AlgorithmType):
            return self.value == other.value

        return False
