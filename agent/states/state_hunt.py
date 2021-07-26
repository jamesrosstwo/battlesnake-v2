from agent.actions.action import get_action_to
from agent.environment.coord import BoardCoord
from agent.singleton import Singleton
from agent.states.state import BattleSnakeState
import random

from agent.states.state_food import BattleSnakeFoodState


def try_hunt_paths(board, entity, heads_by_dist):
    for head in heads_by_dist:
        try:
            try_path = board.get_safe_path(entity.snake.head, head)
            if len(try_path) == 0:
                continue
            return try_path
        except KeyError:
            continue  # No path

    for head in heads_by_dist:
        try:
            try_path = board.get_path(entity.snake.head, head)
            if len(try_path) == 0:
                continue
            return try_path
        except KeyError:
            continue  # No path
    return None


@Singleton
class BattleSnakeHuntState(BattleSnakeState):
    def enter(self, entity):
        pass

    def execute(self, entity):
        board = entity.board

        smaller_snakes = [x for x in board.snakes if x.length + 2 < entity.snake.length]
        smaller_snake_heads = [x.head for x in smaller_snakes]

        # Don't chase after smaller snakes if there aren't many of them
        if len(smaller_snakes) < max(1, (board.num_snakes - 1) / 2):
            entity.state_machine.change_state(BattleSnakeFoodState.instance())
            return entity.state_machine.calculate_action()
        path = try_hunt_paths(board, entity, smaller_snake_heads)
        if path is None:
            entity.state_machine.change_state(BattleSnakeFoodState.instance())
            return entity.state_machine.calculate_action()
        next_node = BoardCoord(*path[0])
        d = next_node - entity.snake.head
        return get_action_to(d)

    def exit(self, entity):
        pass
