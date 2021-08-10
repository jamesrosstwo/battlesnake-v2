from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from agent.action import BattleSnakeAction
from game.state import BattleSnakeGameState


class BattleSnakeAgent:
    def __init__(self):
        self.board = None
        self.snake = None

    def act(self, board_json) -> "BattleSnakeAction":
        self.snake = BattleSnakeSnake.from_dict(board_json["you"])
        metadata = BattleSnakeGameMetadata.from_json(board_json)
        game_state = BattleSnakeGameState.from_json(metadata, board_json, self.snake.name)
        return BattleSnakeAction.RIGHT


