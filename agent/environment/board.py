# Partially taken from https://www.redblobgames.com/pathfinding/a-star/implementation.html

from typing import List, Tuple, Dict, Optional
from agent.data_structures import Queue, PriorityQueue
from agent.environment.cell import BattleSnakeCellType, BattleSnakeCell, cell_symbols
from agent.environment.coord import BoardCoord
from agent.environment.snake import BattleSnakeSnake

i = 0


def _get_snakes_from_json(board_json):
    snake_json = board_json["board"]["snakes"]
    return [BattleSnakeSnake(x) for x in snake_json]


class BattleSnakeBoard:
    def __init__(self, board_json: dict):
        self.width = board_json["board"]["width"]
        self.height = board_json["board"]["height"]
        self.cells = \
            [
                [BattleSnakeCell(x, y, BattleSnakeCellType.EMPTY) for x in range(self.width)]
                for y in range(self.height)
            ]

        self.food = []

        self._add_food(board_json)
        self._add_danger(board_json)
        self.snakes = _get_snakes_from_json(board_json)
        self._add_heads(board_json)
        self.num_snakes = len(self.snakes)

    def get_cell(self, x, y) -> BattleSnakeCell:
        return self.cells[self.height - y - 1][x]

    def get_cell_from_coord(self, coord: BoardCoord):
        return self.get_cell(coord.x, coord.y)

    def _set_cell(self, x, y, t: BattleSnakeCellType):
        self.cells[self.height - y - 1][x] = BattleSnakeCell(x, y, t)

    def _add_food(self, board_json):
        for food in board_json["board"]["food"]:
            current_food = BoardCoord(food["x"], food["y"])
            self._set_cell(current_food.x, current_food.y, BattleSnakeCellType.FOOD)
            self.food.append(current_food)

    def _add_danger(self, board_json):
        for snake in board_json["board"]["snakes"]:
            for body_seg in snake["body"]:
                self._set_cell(body_seg["x"], body_seg["y"], BattleSnakeCellType.DANGER)

    def _add_heads(self, board_json):
        for snake in self.snakes:
            if snake.id == board_json["you"]["id"]:
                continue
            if snake.length + 2 < board_json["you"]["length"]:
                self._set_cell(snake.head.x, snake.head.y, BattleSnakeCellType.EMPTY)
            else:
                for cell in self._diag_neighbours(snake.head):
                    self._set_cell(cell.x, cell.y, BattleSnakeCellType.DANGER)

    def _is_valid(self, pos: BoardCoord):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def _is_safe(self, pos: BoardCoord):
        if not self._is_valid(pos):
            return False
        return self.get_cell_from_coord(pos).type != BattleSnakeCellType.DANGER

    def _is_extra_safe(self, pos: BoardCoord):
        if not self._is_safe(pos):
            return False
        adj_safe = [x for x in self._diag_neighbours(pos) if self.get_cell_from_coord(x).type != BattleSnakeCellType.DANGER]
        return len(adj_safe) >= 3  # Our previous body segment is danger, so only look for three

    def _safe_neighbours(self, pos: BoardCoord) -> List[BoardCoord]:
        return [x for x in self._neighbours(pos) if self._is_safe(x)]

    def _neighbours(self, pos: BoardCoord) -> List[BoardCoord]:
        neighbour_offsets = [BoardCoord(-1, 0), BoardCoord(1, 0), BoardCoord(0, -1), BoardCoord(0, 1)]
        return [pos + x for x in neighbour_offsets if self._is_valid(pos + x)]

    def _diag_neighbours(self, pos: BoardCoord) -> List[BoardCoord]:
        neighbour_offsets = [BoardCoord(-1, 0), BoardCoord(1, 0), BoardCoord(0, -1), BoardCoord(0, 1), BoardCoord(-1, 1), BoardCoord(1, 1), BoardCoord(-1, -1), BoardCoord(1, -1)]
        return [pos + x for x in neighbour_offsets if self._is_valid(pos + x)]

    def _extra_safe_neighbours(self, pos: BoardCoord) -> List[BoardCoord]:
        neighbour_offsets = [BoardCoord(-1, 0), BoardCoord(1, 0), BoardCoord(0, -1), BoardCoord(0, 1)]
        return [pos + x for x in neighbour_offsets if self._is_extra_safe(pos + x)]

    def get_path(self, start: BoardCoord, goal: BoardCoord, neighbour_func=None):
        if not neighbour_func:
            neighbour_func = self._safe_neighbours

        def dijkstra_search():
            frontier = PriorityQueue()
            frontier.put(start.get_tuple(), 0)
            came_from: Dict[Tuple, Optional[Tuple]] = dict()
            cost_so_far: Dict[Tuple, float] = dict()
            came_from[start.get_tuple()] = None
            cost_so_far[start.get_tuple()] = 0

            while not frontier.empty():
                current: Tuple = frontier.get()

                if current == goal.get_tuple():
                    break

                for n in neighbour_func(BoardCoord(*current)):
                    new_cost = cost_so_far[current] + 1
                    if n.get_tuple() not in cost_so_far or new_cost < cost_so_far[n.get_tuple()]:
                        cost_so_far[n.get_tuple()] = new_cost
                        priority = new_cost
                        frontier.put(n.get_tuple(), priority)
                        came_from[n.get_tuple()] = current
            return came_from, cost_so_far

        def reconstruct_path(came_from: Dict[Tuple, Tuple]) -> List[Tuple]:
            current: Tuple = goal.get_tuple()
            path: List[Tuple] = []
            while current != start.get_tuple():
                path.append(current)
                current = came_from[current]
            path.reverse()  # optional
            return path

        c_f, c_s_f = dijkstra_search()
        return reconstruct_path(c_f)

    def get_safe_path(self, start: BoardCoord, goal: BoardCoord):
        return self.get_path(start, goal, neighbour_func=self._extra_safe_neighbours)

    # Manhattan distance because we're locked to a grid
    @staticmethod
    def dist(a: BoardCoord, b: BoardCoord):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def print_board(self):
        print("BOARD: ")
        out_str = ""
        for row in self.cells:
            for cell in row:
                out_str += cell_symbols[cell.type] + " "
            out_str += "\n"
        print(out_str)
