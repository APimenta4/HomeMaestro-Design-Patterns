import random

from . import Feature
from typing import TypedDict

class TemperatureParameters(TypedDict):
    temperature: int


class TemperatureFeature(Feature):
    def __init__(self, name: str, options: TemperatureParameters | None = None):
        super().__init__(name, options)
        self.temperature = options.get("temperature", 0.0)

    def execute(self):
        # Virtual device, therefore we simulate temperature reading
        self.temperature = round(random.uniform(15.0, 25.0))

    def get_status(self):
        return {"temperature": self.temperature}

    def to_dict(self):
        dict = super().to_dict()
        dict["temperature"] = self.temperature
        return dict
