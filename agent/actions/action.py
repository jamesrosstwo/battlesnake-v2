from enum import Enum, auto


class BattleSnakeAction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @staticmethod
    def parse_action(action) -> str:
        return _action_map[action]


def get_action_to(d):
    if d.x > 0:
        return BattleSnakeAction.RIGHT
    elif d.x < 0:
        return BattleSnakeAction.LEFT

    if d.y > 0:
        return BattleSnakeAction.UP
    return BattleSnakeAction.DOWN


_action_map = {
    BattleSnakeAction.UP: "up",
    BattleSnakeAction.DOWN: "down",
    BattleSnakeAction.LEFT: "left",
    BattleSnakeAction.RIGHT: "right",
}
