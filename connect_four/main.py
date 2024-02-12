from algorithms.algorithm_type import AlgorithmType
from game_engine.game_engine import GameEngine
from player.player_type import PlayerType

engine = GameEngine()

engine.create_player("Human", PlayerType.HUMAN)
engine.create_player(
    "AI", PlayerType.AI, False, algorithm_type=AlgorithmType.ALPHA_BETA
)

engine.play()
