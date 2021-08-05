from enum import IntEnum

import numpy as np

from game.coord import BoardCoord


class BattleSnakeCellType(IntEnum):
    EMPTY = 0
    FOOD = 1
    DANGER = 2


cell_symbols = {
    BattleSnakeCellType.DANGER: "D",
    BattleSnakeCellType.FOOD: "F",
    BattleSnakeCellType.EMPTY: "."
}

CELL_DIMS = len(cell_symbols)


class BattleSnakeCell:
    def __init__(self, x, y, type: BattleSnakeCellType):
        self.x = x
        self.y = y
        self.type = type

    def get_pos(self):
        return BoardCoord(self.x, self.y)

    def set_type(self, type: BattleSnakeCellType):
        self.type = type

    """One hot encoded cells"""

    def encode(self) -> np.array:
        vec = np.zeros(CELL_DIMS)
        vec[int(self.type)] = 1
        return vec
