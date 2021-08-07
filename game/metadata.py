import json
from dataclasses import dataclass

from game.utils import BoundingBox, lowercase_keys

@dataclass
class BattleSnakeGameMetadata:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

    @classmethod
    def from_json(cls, turn_json: str):
        turn_json = lowercase_keys(json.loads(turn_json))
        return cls(int(turn_json["game"]["width"]), int(turn_json["game"]["height"]))

    @property
    def bounds(self) -> BoundingBox:
        return BoundingBox(0, 0, self.width - 1, self.height - 1)

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height