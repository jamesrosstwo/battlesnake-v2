from agent.actions.action import get_action_to
from agent.environment.coord import BoardCoord
from agent.singleton import Singleton
from agent.states.state import BattleSnakeState
import random


def try_rand_paths(board, entity):
    path = None
    shuffled_coords = [x.get_pos() for x in [cell for row in board.cells for cell in row]]
    random.shuffle(shuffled_coords)

    for coord in shuffled_coords:
        try:
            try_path = board.get_safe_path(entity.snake.head, coord)
            if len(try_path) == 0:
                continue
            return try_path
        except KeyError:
            continue  # No path

    if path is None:
        for coord in shuffled_coords:
            try:
                try_path = board.get_path(entity.snake.head, coord)
                if len(try_path) == 0:
                    continue
                return try_path
            except KeyError:
                continue  # No path

    return path


@Singleton
class BattleSnakeAvoidState(BattleSnakeState):
    def enter(self, entity):
        pass

    def execute(self, entity):
        board = entity.board

        path = try_rand_paths(board, entity)
        next_node = BoardCoord(*path[0])
        d = next_node - entity.snake.head
        return get_action_to(d)

    def exit(self, entity):
        pass
