from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from agent.action import BattleSnakeAction
from game.state import BattleSnakeGameState


class BattleSnakeAgent:
    def __init__(self):
        self.board = None
        self.snake = None

    def act(self, board_json) -> "BattleSnakeAction":
        print(board_json)
        self.snake = BattleSnakeSnake.from_dict(board_json["you"])
        metadata = BattleSnakeGameMetadata.from_game_board(board_json)

        parsed_board_json = board_json["board"]
        parsed_board_json["turn"] = board_json["turn"]

        game_state = BattleSnakeGameState.from_dict(metadata, parsed_board_json, self.snake.name)
        return BattleSnakeAction.RIGHT


