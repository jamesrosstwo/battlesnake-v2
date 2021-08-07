from dataclasses import dataclass
from typing import List
import pickle

from agent.model.transition import BattleSnakeTransition
from definitions import SETTINGS, ROOT_PATH


def _save_path_from_name(filename):
    return str(ROOT_PATH / SETTINGS["data"]["path"] / filename) + ".pickle"


@dataclass
class BattleSnakeDataset:
    transitions: List[BattleSnakeTransition]

    def save(self, filename):
        save_path = _save_path_from_name(filename)
        pickle.dump(self.transitions, open(save_path, "wb"))

    @classmethod
    def load(cls, filename):
        save_path = _save_path_from_name(filename)
        return cls(pickle.load(open(save_path, "rb")))
