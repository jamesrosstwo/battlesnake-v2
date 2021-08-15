from game.utils import Point


class BattleSnakeSnake:
    def __init__(self, head: Point, id: str, length: int, health: int, name: str):
        self.head_pos: Point = head
        self.id: str = id
        self.length: int = length
        self.health: int = health
        self.name: str = name

    @classmethod
    def from_dict(cls, json: dict):
        head = Point(json["body"][0]["x"], json["body"][0]["y"])
        id = json["id"]
        length = len(json["body"])
        health = json["health"]
        name = json["name"]

        return cls(head, id, length, health, name)
