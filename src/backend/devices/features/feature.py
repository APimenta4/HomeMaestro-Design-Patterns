from abc import ABC, abstractmethod

import paho.mqtt.client as mqtt
from shared import Identifiable


class Feature(Identifiable, ABC):
    def __init__(self, name: str, options: dict[str, object] | None = None):
        super().__init__(name)
        self.options = options or {}

    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def get_status(self) -> None:
        pass

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["options"] = self.options
        return dict
