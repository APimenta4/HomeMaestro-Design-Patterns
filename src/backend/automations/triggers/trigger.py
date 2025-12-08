from abc import ABC, abstractmethod

from .conditions import Condition


class Trigger(ABC):
    def __init__(self, conditions: set[Condition]):
        self.conditions = conditions

    @abstractmethod
    def check_conditions(self, device_id: int, payload: str) -> bool:
        pass

    def to_dict(self) -> dict[str, object]:
        return {
            "conditions": [condition.__class__.__name__ for condition in self.conditions]
        }
    
    def to_dict_deep(self) -> dict[str, object]:
        return {
            "conditions": [condition.to_dict() for condition in self.conditions]
        }
