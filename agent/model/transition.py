from dataclasses import dataclass

from torch import Tensor

@dataclass
class BattleSnakeTransition:
    prev_state: Tensor
    next_state: Tensor
    action: Tensor