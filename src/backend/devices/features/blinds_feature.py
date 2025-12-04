import random

from . import Feature
from typing import TypedDict

class BlindsParameters(TypedDict):
    position: float

class BlindsFeature(Feature):
    def __init__(self, name: str, options: BlindsParameters | None = None):
        super().__init__(name, options)
        self.position = options.get("position", 0.0)  # fully open

    def execute(self):
        # Virtual device, therefore we simulate how much the blinds will be opened
        self.position = round(random.uniform(0.0, 1.0), 2)

    def get_status(self):
        return {"position": self.position}

    def to_dict(self):
        dict = super().to_dict()
        dict["position"] = self.position
        return dict
