from abc import ABC, abstractmethod


class Condition(ABC):
    def __init__(
        self, device_id: int, feature_id: int, options: dict[str, object] | None = None
    ):
        self.options = options or {}
        self.device_id = device_id
        self.feature_id = feature_id

    @abstractmethod
    def check(self, device_id: int, payload: str) -> bool:
        if self.device_id != device_id:
            return False
        # ...

    def to_dict(self) -> dict[str, object]:
        return {
            "device_id": self.device_id,
            "feature_id": self.feature_id,
        }
