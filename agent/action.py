from enum import IntEnum

import torch

from definitions import TORCH_DEVICE
from game.state import BattleSnakeGameState


class BattleSnakeAction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def parse_action(action) -> str:
        action_map = {
            BattleSnakeAction.UP: "up",
            BattleSnakeAction.DOWN: "down",
            BattleSnakeAction.LEFT: "left",
            BattleSnakeAction.RIGHT: "right",
        }

        return action_map[action]

    @classmethod
    def from_states(cls, prev_state: BattleSnakeGameState, next_state: BattleSnakeGameState):
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
        action_vals = [0 for _ in range(len(BattleSnakeAction))]
        action_vals[int(self)] = 1
        return torch.tensor(action_vals, dtype=torch.long, device=TORCH_DEVICE)


def get_action_to(d):
    if d.x > 0:
        return BattleSnakeAction.RIGHT
    elif d.x < 0:
        return BattleSnakeAction.LEFT

    if d.y > 0:
        return BattleSnakeAction.UP
    return BattleSnakeAction.DOWN
