from abc import ABC, abstractmethod
from enum import Enum

import paho.mqtt.client as mqtt
from shared import Identifiable


class FeatureCategory(Enum):
    ACTUATOR = "ACTUATOR"
    SENSOR = "SENSOR"


class Feature(Identifiable, ABC):
    def __init__(self, name: str, category: FeatureCategory, options: dict[str, object] | None = None):
        super().__init__(name)
        self.options = options or {}
        self.category = category

    @abstractmethod
    def execute(self, options: dict[str, object] | None = None) -> str:
        pass

    @abstractmethod
    def get_status(self) -> None:
        pass

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["options"] = self.options
        dict["category"] = self.category.value
        return dict
