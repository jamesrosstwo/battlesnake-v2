from enum import Enum, auto

from game.turn import BattleSnakeTurn


class BattleSnakeAction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @staticmethod
    def parse_action(action) -> str:
        return _action_map[action]

    @classmethod
    def from_states(cls, prev_state: BattleSnakeTurn, next_state: BattleSnakeTurn):
        prev_pos = prev_state.our_snake.head_pos
        next_pos = next_state.our_snake.head_pos
        diff = next_pos - prev_pos
        if diff.y > 0:
            return BattleSnakeAction.UP
        if diff.y < 0:
            return BattleSnakeAction.DOWN
        if diff.x > 0:
            return BattleSnakeAction.RIGHT
        if diff.x < 0:
            return BattleSnakeAction.LEFT


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
