from abc import ABC, abstractmethod
from triggers.conditions import Condition


class Trigger(ABC):
    def __init__(self, conditions: set[Condition]):
        self.conditions = conditions

    @abstractmethod
    def check_conditions(self) -> bool:
        pass
