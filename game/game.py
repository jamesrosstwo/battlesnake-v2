"""
A collection of battlesnake board states that make up a game
"""
from typing import List

from game.board import BattleSnakeBoard
from game.metadata import BattleSnakeGameMetadata
from game.turn import BattleSnakeTurn


class BattleSnakeGame:
    def __init__(self, metadata: BattleSnakeGameMetadata, states: List[BattleSnakeTurn]):
        self.metadata = metadata
        self.states = states

    @classmethod
    def from_json(cls, metadata_json: str, turns_json: List[str], snake_name: str):
        metadata = BattleSnakeGameMetadata.from_json(metadata_json)
        turns = [BattleSnakeTurn.from_json(metadata, turn, snake_name) for turn in turns_json]
        return cls(metadata, turns)