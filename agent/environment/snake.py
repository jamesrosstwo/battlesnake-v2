from agent.environment.coord import BoardCoord


class BattleSnakeSnake:
    def __init__(self, json):
        self.head = BoardCoord(json["head"]["x"], json["head"]["y"])
        self.id = json["id"]
        self.length = json["length"]
        self.health = json["health"]