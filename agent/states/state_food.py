from agent.actions.action import get_action_to
from agent.environment.board import BattleSnakeBoard
from agent.environment.coord import BoardCoord
from agent.singleton import Singleton
from agent.states.state import BattleSnakeState
from agent.states.state_avoid import BattleSnakeAvoidState


def try_safe_food_paths(board, entity, food_by_dist):
    for food in food_by_dist:
        try:
            try_path = board.get_safe_path(entity.snake.head, food)
            if len(try_path) == 0:
                continue
            return try_path
        except KeyError:
            continue  # No path
    return None


def try_food_paths(board, entity, food_by_dist):
    for food in food_by_dist:
        try:
            try_path = board.get_path(entity.snake.head, food)
            if len(try_path) == 0:
                continue
            return try_path
        except KeyError:
            continue  # No path
    return None


@Singleton
class BattleSnakeFoodState(BattleSnakeState):
    def enter(self, entity):
        pass

    def execute(self, entity):
        board = entity.board
        food_by_dist = sorted(board.food, key=lambda x: BattleSnakeBoard.dist(entity.snake.head, x))

        path = try_safe_food_paths(board, entity, food_by_dist)
        if path is None:
            smaller_snakes = [x for x in board.snakes if x.length < entity.snake.length]
            if len(smaller_snakes) < min(1, (board.num_snakes - 1)) or entity.snake.health < 40:
                path = try_food_paths(board, entity, food_by_dist)

        if path is None:
            entity.state_machine.change_state(BattleSnakeAvoidState.instance())
            return entity.state_machine.calculate_action()
        next_node = BoardCoord(*path[0])
        d = next_node - entity.snake.head
        return get_action_to(d)

    def exit(self, entity):
        pass
