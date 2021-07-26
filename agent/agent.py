from agent.environment.board import BattleSnakeBoard, BoardCoord
from agent.environment.snake import BattleSnakeSnake
from agent.state_machine import BattleSnakeStateMachine
from agent.actions.action import BattleSnakeAction
from agent.states.state_food import BattleSnakeFoodState
from agent.states.state_hunt import BattleSnakeHuntState


class BattleSnakeAgent:
    def __init__(self):
        self.state_machine = BattleSnakeStateMachine(self)
        self.board = None
        self.snake = None

    def select_state(self, board) -> "BattleSnakeState":
        pass

    def parse_board(self, board):
        pass

    def act(self, board_json) -> "BattleSnakeAction":
        self.board = BattleSnakeBoard(board_json)
        self.snake = BattleSnakeSnake(board_json["you"])
        self.state_machine.change_state(BattleSnakeHuntState.instance())
        return self.state_machine.calculate_action()

from agent.states.state import BattleSnakeState
