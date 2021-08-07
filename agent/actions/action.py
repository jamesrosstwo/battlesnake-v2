from enum import Enum, auto, IntEnum

import torch

from definitions import TORCH_DEVICE
from game.turn import BattleSnakeTurn


class BattleSnakeAction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

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
        elif diff.y < 0:
            return BattleSnakeAction.DOWN
        elif diff.x > 0:
            return BattleSnakeAction.RIGHT
        elif diff.x < 0:
            return BattleSnakeAction.LEFT
        else:
            return BattleSnakeAction.UP


    def to_tensor(self) -> torch.Tensor:
        action_vals = [0, 0, 0, 0]
        action_vals[int(self)] = 1
        return torch.tensor(action_vals, dtype=torch.float32, device=TORCH_DEVICE)

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
