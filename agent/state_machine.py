from agent.actions.action import BattleSnakeAction
from agent.states.state_food import BattleSnakeFoodState


class BattleSnakeStateMachine:
    def __init__(self, owner):
        self.owner = owner
        self.current_state: "BattleSnakeState" = BattleSnakeFoodState.instance()
        self.previous_state: "BattleSnakeState" = None

    def change_state(self, new_state: "BattleSnakeState"):
        self.previous_state = self.current_state
        if self.current_state:
            self.current_state.exit(self.owner)
        self.current_state = new_state
        if self.current_state:
            self.current_state.enter(self.owner)

    def calculate_action(self) -> BattleSnakeAction:
        return self.current_state.execute(self.owner)

    def revert_to_last_state(self):
        if self.previous_state:
            self.change_state(self.previous_state)


from agent.states.state import BattleSnakeState

