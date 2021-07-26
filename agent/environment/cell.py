from enum import Enum, auto
from agent.environment.coord import BoardCoord


class BattleSnakeCellType(Enum):
    DANGER = auto()
    FOOD = auto()
    EMPTY = auto()


cell_symbols = {
    BattleSnakeCellType.DANGER: "D",
    BattleSnakeCellType.FOOD: "F",
    BattleSnakeCellType.EMPTY: "."
}


class BattleSnakeCell:
    def __init__(self, x, y, type: BattleSnakeCellType):
        self.x = x
        self.y = y
        self.type = type

    def get_pos(self):
        return BoardCoord(self.x, self.y)

