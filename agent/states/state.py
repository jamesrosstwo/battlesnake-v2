from abc import ABC, abstractmethod

from agent.actions.action import BattleSnakeAction



class BattleSnakeState(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def enter(self, entity):
        pass

    @abstractmethod
    def execute(self, entity) -> BattleSnakeAction:
        pass

    @abstractmethod
    def exit(self, entity):
        pass

