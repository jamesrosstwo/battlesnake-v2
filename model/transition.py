from typing import List

from game.board import BattleSnakeBoard
from game.game import BattleSnakeGame


class BattleSnakeTransition:
    def __init__(self, prev_state: BattleSnakeBoard, next_state: BattleSnakeBoard):
        pass


def create_transitions_from_game(game: BattleSnakeGame) -> List[BattleSnakeTransition]:
    pass
