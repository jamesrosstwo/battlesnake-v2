from dataclasses import dataclass

from torch import Tensor

from agent.actions.action import BattleSnakeAction


@dataclass
class BattleSnakeTransition:
    prev_state: Tensor
    next_state: Tensor
    action: BattleSnakeAction