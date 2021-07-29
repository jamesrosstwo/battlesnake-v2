from typing import List

from data_generator.dataset import BattleSnakeDataset
from game.game import BattleSnakeGame
from model.transition import BattleSnakeTransition


class BattleSnakeDataGenerator:
    def __init__(self):
        pass

    def _generate_transitions_from_game(self, game: BattleSnakeGame) -> List[BattleSnakeTransition]:
        pass

    def generate_data(self, games: List[BattleSnakeGame]) -> BattleSnakeDataset:
        out_games: List[BattleSnakeTransition] = []
        for game in games:
            out_games += self._generate_transitions_from_game(game)
        return BattleSnakeDataset(out_games)