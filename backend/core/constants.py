"""
File: constants.py
Project: Backend - Connect Four
File Created: Wednesday, 24th July 2024 8:36:03 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The constants for the system.
-----
Last Modified: Wednesday, 24th July 2024 8:36:34 AM
Modified By: feaad
-----
Copyright ©2024 feaad
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# The default number of rows and columns for the Connect Four board.
DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7

# The number associated with each player.
PLAYER_ONE = 1
PLAYER_TWO = 2
RANDOM = 3
EMPTY = 0

# The number of connections needed to win the game.
CONNECT = 4


BACKENDS = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
]
