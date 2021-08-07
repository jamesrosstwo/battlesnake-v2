"""
A collection of battlesnake board states that make up a game
"""
from typing import List

from agent.actions.action import BattleSnakeAction
from agent.model.transition import BattleSnakeTransition
from game.metadata import BattleSnakeGameMetadata
from game.turn import BattleSnakeTurn


class BattleSnakeGame:
    def __init__(self, metadata: BattleSnakeGameMetadata, states: List[BattleSnakeTurn]):
        self.metadata = metadata
        self.states = states
        self.transitions = self._create_transitions()

    @classmethod
    def from_json(cls, metadata_json: str, turns_json: List[str], snake_name: str):
        metadata = BattleSnakeGameMetadata.from_json(metadata_json)
        turns = [BattleSnakeTurn.from_json(metadata, turn, snake_name) for turn in turns_json]
        return cls(metadata, turns)

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
