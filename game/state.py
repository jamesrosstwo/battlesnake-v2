import json
import math
from typing import List

import numpy as np
import torch

from definitions import TORCH_DEVICE
from game.cell import BattleSnakeCell, BattleSnakeCellType
from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from game.utils import Point, lowercase_keys


def _get_snakes_from_board_json(board_json):
    snake_json = board_json["board"]["snakes"]
    return [BattleSnakeSnake.from_dict(x) for x in snake_json]


class BattleSnakeGameState:
    NUM_CHANNELS = BattleSnakeCell.CELL_DIMS


    def __init__(self, local_cells: List[List[BattleSnakeCell]], width: int, height: int, turn_num: int,
                 player: BattleSnakeSnake):
        self.local_cells: List[List[BattleSnakeCell]] = local_cells
        self._width = width
        self._height = height
        self.turn_num = turn_num
        self.our_snake: BattleSnakeSnake = player
        self.tensor: torch.Tensor = self._to_tensor()

    @classmethod
    def from_json(cls, metadata: BattleSnakeGameMetadata, turn_json: str, snake_name: str):
        turn_json = lowercase_keys(json.loads(turn_json))
        turn_num = int(turn_json["turn"])

        cells = \
            [
                [BattleSnakeCell(x, y, BattleSnakeCellType.EMPTY) for y in range(metadata.height)]
                for x in range(metadata.width)
            ]

        for food in turn_json["food"]:
            cells[int(food["x"])][int(food["y"])].set_type(BattleSnakeCellType.FOOD)

        our_snake = None

        for snake in turn_json["snakes"]:
            if snake["name"] == snake_name:
                our_snake = BattleSnakeSnake.from_dict(snake)
            for body_seg in snake["body"]:
                seg_x = int(body_seg["x"])
                seg_y = int(body_seg["y"])
                if not metadata.bounds.contains_point_incl(Point(seg_y, seg_x)):
                    break
                cells[seg_x][seg_y].set_type(BattleSnakeCellType.DANGER)

        return cls(cells, metadata.width, metadata.height, turn_num, our_snake)

    def _to_tensor(self) -> torch.Tensor:
        # Convert BattleSnakeCells to numpy array
        ndarr: np.ndarray = np.zeros((self._width, self._height, BattleSnakeGameState.NUM_CHANNELS))
        for x in range(self._height):
            for y in range(self._width):
                ndarr[x, y] = self.local_cells[x][y].encode()

        # Center view around player
        board_center = (math.ceil(self._width / 2), math.ceil(self._height / 2))
        center_shift = (self.our_snake.head_pos.x - board_center[0], self.our_snake.head_pos.y - board_center[1])
        centered_input = np.roll(ndarr, center_shift, (0, 1))
        return torch.from_numpy(centered_input).float().to(TORCH_DEVICE)
