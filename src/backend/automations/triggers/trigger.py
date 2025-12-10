from abc import ABC, abstractmethod

from .conditions import Condition


class Trigger(ABC):
    def __init__(self, conditions: set[Condition]):
        self.conditions = conditions

    def check_conditions(self, device_id: int, payload: str) -> bool:
        if not self.is_interested_in_event(device_id, payload):
            return False

        for condition in self.conditions:
            if not condition.check(device_id, payload):
                return False
        return True
    
    def is_interested_in_event(self, device_id: int, payload: str) -> bool:
        for condition in self.conditions:
            if condition.is_interested_in_event(device_id, payload):
                return True

        return False

    def to_dict(self) -> dict[str, object]:
        return {
            "conditions": [
                condition.__class__.__name__ for condition in self.conditions
            ]
        }

    def to_dict_deep(self) -> dict[str, object]:
        return {"conditions": [condition.to_dict() for condition in self.conditions]}
