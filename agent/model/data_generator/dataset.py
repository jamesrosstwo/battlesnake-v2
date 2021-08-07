from dataclasses import dataclass
from typing import List
import pickle

from agent.model.data_generator.transition import BattleSnakeTransition
from definitions import SETTINGS, ROOT_PATH
from game.game import BattleSnakeGame
from game.metadata import BattleSnakeGameMetadata


def _save_path_from_name(filename):
    return str(ROOT_PATH / SETTINGS["data"]["path"] / filename) + ".pickle"


@dataclass
class BattleSnakeDataset:
    metadata: BattleSnakeGameMetadata
    transitions: List[BattleSnakeTransition]


    def save(self, filename):
        save_path = _save_path_from_name(filename)
        pickle.dump(self, open(save_path, "wb"))

    @classmethod
    def load(cls, filename):
        save_path = _save_path_from_name(filename)
        return pickle.load(open(save_path, "rb"))

    @classmethod
    def from_games(cls, games: List[BattleSnakeGame]):
        assert(len(games) > 0)
        out_transitions: List[BattleSnakeTransition] = [games[0].transitions]
        metadata = games[0].metadata
        for game in games[1:]:
            out_transitions.extend(game.transitions)
            assert(game.metadata == metadata)
        return cls(metadata, out_transitions)
