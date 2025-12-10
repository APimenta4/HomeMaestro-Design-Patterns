import json
from abc import ABC, abstractmethod


class Condition(ABC):
    def __init__(
        self, device_id: int, feature_id: int, options: dict[str, object] | None = None
    ):
        self.options = options or {}
        self.device_id = device_id
        self.feature_id = feature_id
        self.evaluation = False

    def is_interested_in_event(self, device_id: int, payload: str) -> bool:
        data: dict[str, object] = json.loads(payload)

        return self.device_id == device_id and data.get("id") == self.feature_id

    def check(self, device_id: int, payload: str) -> bool:
        data: dict[str, object] = json.loads(payload)

        if self.device_id == device_id and data.get("id") == self.feature_id:
            self.evaluate(data)
        
        return self.evaluation

    @abstractmethod
    def evaluate(self, data: dict[str, object]) -> bool:
        pass

    def to_dict(self) -> dict[str, object]:
        return {
            "device_id": self.device_id,
            "feature_id": self.feature_id,
            "evaluation": self.evaluation,
        }
