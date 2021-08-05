import json
from typing import List

import numpy as np
import torch

from game.cell import BattleSnakeCell, BattleSnakeCellType, CELL_DIMS
from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from game.utils import Point


def _get_snakes_from_board_json(board_json):
    snake_json = board_json["board"]["snakes"]
    return [BattleSnakeSnake(x) for x in snake_json]


class BattleSnakeTurn:
    def __init__(self, local_cells: List[List[BattleSnakeCell]], width: int, height: int):
        self.local_cells: List[List[BattleSnakeCell]] = local_cells
        self._width = width
        self._height = height
        self.tensor: torch.Tensor = self._to_tensor()

    @classmethod
    def from_json(cls, metadata: BattleSnakeGameMetadata, turn_json: str, snake_name: str):
        turn_json = json.loads(turn_json)

        cells = \
            [
                [BattleSnakeCell(x, y, BattleSnakeCellType.EMPTY) for y in range(metadata.height)]
                for x in range(metadata.width)
            ]

        for food in turn_json["Food"]:
            cells[int(food["X"])][int(food["Y"])].set_type(BattleSnakeCellType.FOOD)

        for snake in turn_json["Snakes"]:
            for body_seg in snake["Body"]:
                seg_x = int(body_seg["X"])
                seg_y = int(body_seg["Y"])
                if not metadata.bounds.contains_point_incl(Point(seg_y, seg_x)):
                    break
                cells[seg_x][seg_y].set_type(BattleSnakeCellType.DANGER)

        return cls(cells, metadata.width, metadata.height)

    def _to_tensor(self) -> torch.Tensor:
        ndarr: np.ndarray = np.zeros((self._width, self._height, CELL_DIMS))
        for x in range(self._height):
            for y in range(self._width):
                ndarr[x, y] = self.local_cells[x][y].encode()
        return torch.from_numpy(ndarr)
