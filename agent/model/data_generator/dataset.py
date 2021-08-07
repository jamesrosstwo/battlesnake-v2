from dataclasses import dataclass
from typing import List
import pickle

from agent.model.transition import BattleSnakeTransition
from definitions import SETTINGS, ROOT_PATH


@dataclass
class BattleSnakeDataset:
    transitions: List[BattleSnakeTransition]

    def save(self, filename):
        save_path = str(ROOT_PATH / SETTINGS["data"]["path"] / filename)
        pickle.dump(self.transitions, open(save_path, "wb"))

