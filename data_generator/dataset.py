from dataclasses import dataclass
from typing import List

from model.transition import BattleSnakeTransition


@dataclass
class BattleSnakeDataset:
    transitions: List[BattleSnakeTransition]

    def save(self, path):
        pass
