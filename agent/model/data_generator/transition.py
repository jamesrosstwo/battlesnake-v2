from dataclasses import dataclass

from torch import Tensor

@dataclass
class BattleSnakeTransition:
    prev_state: Tensor
    next_state: Tensor
    action: Tensor


    def __iter__(self):
        yield self.prev_state
        yield self.next_state
        yield self.action