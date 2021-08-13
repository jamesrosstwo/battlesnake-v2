from typing import Tuple

import numpy as np
import torch

from agent.model.model import BattleSnakeConvNet
from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from agent.action import BattleSnakeAction
from game.state import BattleSnakeGameState, _display_state_tensor


def coords_from_dir(dir: str) -> Tuple[int, int]:
  if dir == "up":
    return (0, 1)
  if dir == "down":
    return (0, -1)
  if dir == "left":
    return (-1, 0)
  if dir == "right":
    return (1, 0)

class BattleSnakeAgent:
    def __init__(self, conv_net: BattleSnakeConvNet):
        self.board = None
        self.snake = None
        self.conv_net = conv_net

    def act(self, board_json) -> "BattleSnakeAction":
        self.snake = BattleSnakeSnake.from_dict(board_json["you"])
        metadata = BattleSnakeGameMetadata.from_game_board(board_json)

        parsed_board_json = board_json["board"]
        parsed_board_json["turn"] = board_json["turn"]

        game_state = BattleSnakeGameState.from_dict(metadata, parsed_board_json, self.snake.name)

        board_tensor: torch.Tensor = torch.unsqueeze(game_state.tensor, 0)
        with torch.no_grad():
            action: torch.Tensor = self.conv_net(board_tensor)

        print(action, action.argmax())

        possible_moves = ["up", "down", "left", "right"]
        move_scores = action.tolist()[0]

        my_head = board_json['you']['head']
        my_id = board_json['you']['id']
        board_height = board_json['board']['height']
        board_width = board_json['board']['width']
        snakes = board_json['board']['snakes']

        for idx, move in enumerate(possible_moves):
            new_x = my_head["x"] + coords_from_dir(move)[0]
            new_y = my_head["y"] + coords_from_dir(move)[1]
            new_head_pos = {"x": new_x, "y": new_y}
            if new_x < 0 or new_x > (board_width - 1):
                move_scores[idx] = np.NINF
            if new_y < 0 or new_y > (board_height - 1):
                move_scores[idx] = np.NINF
            for snake in snakes:
                is_our_snake = my_id[:20] == snake['id'][:20]
                in_our_body = is_our_snake and new_head_pos in snake["body"][1:]
                in_their_body = not is_our_snake and new_head_pos in snake["body"]
                if in_our_body or in_their_body:
                    move_scores[idx] = -np.inf

        return BattleSnakeAction(int(np.argmax(move_scores)))


