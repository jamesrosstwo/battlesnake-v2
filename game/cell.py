from enum import IntEnum

import numpy as np

from game.coord import BoardCoord


class BattleSnakeCellType(IntEnum):
    EMPTY = 0
    FOOD = 1
    DANGER = 2
    WALL = 3


class BattleSnakeCell:
    CELL_DIMS = len(BattleSnakeCellType) - 1

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
        vec = np.zeros(BattleSnakeCell.CELL_DIMS)
        int_t = int(self.type)
        if int_t > 0:
            vec[int(self.type) - 1] = 1
        return vec
