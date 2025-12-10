import json

from . import Feature, FeatureCategory
from typing import TypedDict

class TemperatureParameters(TypedDict):
    temperature: float


class TemperatureFeature(Feature):
    def __init__(self, name: str, category: FeatureCategory, options: TemperatureParameters | None = None):
        super().__init__(name, category, options)
        self.temperature = options.get("temperature", 0.0)

    def execute(self, options: TemperatureParameters | None = None):
        if options and "temperature" in options and options["temperature"] is not None:
            self.temperature = float(options.get("temperature", self.temperature))
            if self.options:
                self.options["temperature"] = self.temperature
        return json.dumps(self.to_dict())

    def get_status(self):
        return {"temperature": self.temperature}

    def to_dict(self):
        dict = super().to_dict()
        dict["temperature"] = self.temperature
        return dict
