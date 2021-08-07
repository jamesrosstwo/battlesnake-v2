"""
A collection of battlesnake board states that make up a game
"""
from typing import List

from agent.action import BattleSnakeAction
from agent.model.data_generator.transition import BattleSnakeTransition
from game.metadata import BattleSnakeGameMetadata
from game.state import BattleSnakeGameState


class BattleSnakeGame:
    def __init__(self, metadata: BattleSnakeGameMetadata, states: List[BattleSnakeGameState]):
        self.metadata = metadata
        self.states: List[BattleSnakeGameState] = states
        self.transitions = self._create_transitions()

    @classmethod
    def from_json(cls, metadata_json: str, turns_json: List[str], snake_name: str):
        metadata = BattleSnakeGameMetadata.from_json(metadata_json)
        states = [BattleSnakeGameState.from_json(metadata, turn, snake_name) for turn in turns_json]
        return cls(metadata, states)

    def _create_transitions(self) -> List[BattleSnakeTransition]:
        out_transitions: List[BattleSnakeTransition] = []
        for idx in range(len(self.states))[:-1]:
            prev_state = self.states[idx]
            next_state = self.states[idx + 1]
            action = BattleSnakeAction.from_states(prev_state, next_state)
            out_transitions.append(BattleSnakeTransition(
                prev_state.tensor,
                next_state.tensor,
                action.to_tensor()
            ))
        return out_transitions
