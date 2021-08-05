import json
from typing import List

from game.cell import BattleSnakeCell, BattleSnakeCellType
from game.metadata import BattleSnakeGameMetadata
from game.snake import BattleSnakeSnake
from game.utils import Point


def _get_snakes_from_board_json(board_json):
    snake_json = board_json["board"]["snakes"]
    return [BattleSnakeSnake(x) for x in snake_json]


class BattleSnakeTurn:
    def __init__(self, local_cells: List[List[BattleSnakeCell]]):
        self.local_cells: List[List[BattleSnakeCell]] = local_cells

    @classmethod
    def from_json(cls, metadata: BattleSnakeGameMetadata, turn_json: str, snake_name: str):
        turn_json = json.loads(turn_json)
        print(turn_json)

        cells = \
            [
                [BattleSnakeCell(x, y, BattleSnakeCellType.EMPTY) for x in range(metadata.width)]
                for y in range(metadata.height)
            ]

        for food in turn_json["Food"]:
            cells[int(food["Y"])][int(food["X"])].set_type(BattleSnakeCellType.FOOD)

        for snake in turn_json["Snakes"]:
            print("snake----")
            for body_seg in snake["Body"]:
                seg_x = int(body_seg["X"])
                seg_y = int(body_seg["Y"])
                if not metadata.bounds.contains_point_incl(Point(seg_x, seg_y)):
                    break
                print(seg_x, seg_y)
                cells[seg_y][seg_x].set_type(BattleSnakeCellType.DANGER)

        return cls(cells)
