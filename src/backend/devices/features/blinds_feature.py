import random

from . import Feature, FeatureCategory
from typing import TypedDict

class BlindsParameters(TypedDict):
    position: int

class BlindsFeature(Feature):
    def __init__(self, name: str, category: FeatureCategory, options: BlindsParameters | None = None):
        super().__init__(name, category, options)
        self.position = options.get("position", 0)  # fully open

    def execute(self, options: BlindsParameters | None = None):
        if options and "position" in options:
            self.position = int(options.get("position", self.position))
            if self.options:
                self.options["position"] = self.position
        return f"Blinds position set to {self.position}"

    def get_status(self):
        return {"position": self.position}

    def to_dict(self):
        dict = super().to_dict()
        dict["position"] = self.position
        return dict
