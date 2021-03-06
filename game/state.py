import json
import pickle
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import torch
from torchvision import transforms

from definitions import TORCH_DEVICE, ROOT_PATH
from game.cell import BattleSnakeCell, BattleSnakeCellType
from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from game.utils import Point, lowercase_keys


def _get_snakes_from_board_json(board_json):
    snake_json = board_json["board"]["snakes"]
    return [BattleSnakeSnake.from_dict(x) for x in snake_json]


def _display_state_tensor(x, name: str = "state_img"):
    x = x.to(TORCH_DEVICE).cpu().numpy()
    save_pth = str(ROOT_PATH / "state_tensors" / name)
    img_vals = (x / 2) + 0.5
    # np.save(save_pth, img_vals)
    img_vals = np.moveaxis(img_vals, 0, 2)

    plt.imshow(img_vals[::2])
    plt.show()


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
        return cls.from_dict(metadata, turn_json, snake_name)

    @classmethod
    def from_dict(cls, metadata: BattleSnakeGameMetadata, turn_dict: dict, snake_name: str):
        turn_num = int(turn_dict["turn"])

        cells = \
            [
                [BattleSnakeCell(x, y, BattleSnakeCellType.EMPTY) for y in range(metadata.height)]
                for x in range(metadata.width)
            ]

        for food in turn_dict["food"]:
            cells[int(food["x"])][int(food["y"])].set_type(BattleSnakeCellType.FOOD)

        our_snake = None

        for snake in turn_dict["snakes"]:
            if snake["name"] == snake_name:
                our_snake = BattleSnakeSnake.from_dict(snake)

        for snake in turn_dict["snakes"]:
            for idx, body_seg in enumerate(snake["body"]):
                seg_x = int(body_seg["x"])
                seg_y = int(body_seg["y"])
                if not metadata.bounds.contains_point_incl(Point(seg_y, seg_x)):
                    break
                cells[seg_x][seg_y].set_type(BattleSnakeCellType.SNAKE)
                if idx == 0:
                    d = len(snake["body"]) - our_snake.length
                    cells[seg_x][seg_y].value = int(d >= 0)
                else:
                    cells[seg_x][seg_y].set_type(BattleSnakeCellType.SNAKE_HEAD)

        return cls(cells, metadata.width, metadata.height, turn_num, our_snake)

    def _to_tensor(self) -> torch.Tensor:

        t_w = self._width * 2 - 1
        t_h = self._height * 2 - 1
        # Convert BattleSnakeCells to numpy array
        ndarr: np.ndarray = np.zeros((BattleSnakeGameState.NUM_CHANNELS, t_w, t_h))

        # Fill with wall to get board bounds
        for x in range(t_w):
            for y in range(t_h):
                ndarr[:, x, y] = BattleSnakeCell(x, y, BattleSnakeCellType.WALL).encode()
        for x in range(self._height):
            for y in range(self._width):
                ndarr[:, x, y] = self.local_cells[x][y].encode()

        # Center view around player
        board_center = (t_w // 2, t_h // 2)
        center_shift = (board_center[0] - self.our_snake.head_pos.x, board_center[1] - self.our_snake.head_pos.y)
        centered_input = np.roll(ndarr, center_shift, (1, 2))
        tensor = torch.from_numpy(centered_input).float().to(TORCH_DEVICE)
        means = (0.5, 0.5, 0.5, 0.5)
        stds = (0.5, 0.5, 0.5, 0.5)
        normalized = transforms.Normalize(means, stds)(tensor)
        # _display_state_tensor(normalized)
        return normalized


