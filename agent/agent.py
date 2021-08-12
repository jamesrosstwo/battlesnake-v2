import torch

from agent.model.model import BattleSnakeConvNet
from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from agent.action import BattleSnakeAction
from game.state import BattleSnakeGameState, _display_state_tensor


class BattleSnakeAgent:
    def __init__(self, conv_net: BattleSnakeConvNet):
        self.board = None
        self.snake = None
        self.conv_net = conv_net

    def act(self, board_json) -> "BattleSnakeAction":
        print(board_json)
        self.snake = BattleSnakeSnake.from_dict(board_json["you"])
        metadata = BattleSnakeGameMetadata.from_game_board(board_json)

        parsed_board_json = board_json["board"]
        parsed_board_json["turn"] = board_json["turn"]

        game_state = BattleSnakeGameState.from_dict(metadata, parsed_board_json, self.snake.name)
        _display_state_tensor(game_state.tensor, "state_img_" + str(board_json["turn"]) + ".png")

        board_tensor: torch.Tensor = torch.unsqueeze(game_state.tensor, 0)
        with torch.no_grad():
            action: torch.Tensor = self.conv_net(board_tensor)

        print(action, action.argmax())
        return BattleSnakeAction(int(action.argmax()))


