import json
from dataclasses import dataclass

from game.utils import BoundingBox

"""as     "ID": "0fda03b7-080f-4834-b011-937d1bd51f93",
    "Status": "complete",
    "Width": 11,
    "Height": 11,
    "Ruleset": {
      "foodSpawnChance": "15",
      "minimumFood": "1",
      "name": "standard"
    },
    "SnakeTimeout": 500"""

@dataclass
class BattleSnakeGameMetadata:
    def __init__(self, width: int, height: int, id: str):
        self.width: int = width
        self.height: int = height
        self.id: str = id

    @classmethod
    def from_json(cls, turn_json: str):
        turn_json = json.loads(turn_json)
        return cls(int(turn_json["Game"]["Width"]), int(turn_json["Game"]["Height"]), turn_json["Game"]["ID"])

    @property
    def bounds(self) -> BoundingBox:
        return BoundingBox(0, 0, self.width - 1, self.height - 1)