from typing import List

from agent.model.data_generator.dataset import BattleSnakeDataset
from game.game import BattleSnakeGame
from agent.model.transition import BattleSnakeTransition


class BattleSnakeDataGenerator:
    def __init__(self):
        pass

    def generate_data(self, games: List[BattleSnakeGame]) -> BattleSnakeDataset:
        out_transitions: List[BattleSnakeTransition] = []
        for game in games:
            out_transitions.extend(game.transitions)
        return BattleSnakeDataset(out_transitions)