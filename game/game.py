"""
A collection of battlesnake board states that make up a game
"""
import json
from typing import List, Union, Tuple

from agent.action import BattleSnakeAction
from agent.model.data_generator.transition import BattleSnakeTransition
from game.metadata import BattleSnakeGameMetadata
from game.state import BattleSnakeGameState


class BattleSnakeGame:
    def __init__(self, metadata: BattleSnakeGameMetadata, states: List[BattleSnakeGameState], raw_json=None):
        self.metadata = metadata
        self.states: List[BattleSnakeGameState] = states
        self.action_counts, self.transitions = self._create_transitions()
        self.raw_json = raw_json
        if self.raw_json == None:
            self.raw_json = []

    @classmethod
    def from_json(cls, metadata_json: str, turns_json: List[str], snake_name: str):
        metadata = BattleSnakeGameMetadata.from_json(metadata_json)
        states = [BattleSnakeGameState.from_json(metadata, turn, snake_name) for turn in turns_json]
        turns_json = [x + "\n" for x in turns_json]
        raw_dict = {"metadata": json.loads(metadata_json), "turns": [json.loads(x) for x in turns_json]}
        return cls(metadata, states, json.dumps(raw_dict) + "\n")

    def _create_transitions(self) -> Tuple[List[int], List[BattleSnakeTransition]]:
        counts = [0 for _ in range(4)]
        out_transitions: List[BattleSnakeTransition] = []
        for idx in range(len(self.states))[:-1]:
            prev_state = self.states[idx]
            next_state = self.states[idx + 1]
            action = BattleSnakeAction.from_states(prev_state, next_state)
            if action == None:
                continue
            out_transitions.append(BattleSnakeTransition(
                prev_state.tensor,
                next_state.tensor,
                action.to_tensor(),
                idx
            ))
            counts[int(action)] += 1
        return counts, out_transitions
