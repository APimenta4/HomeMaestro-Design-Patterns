import json

from . import Feature, FeatureCategory
from typing import TypedDict

class LampParameters(TypedDict):
    state: bool
    brightness: int

class LampFeature(Feature):
    def __init__(self, name: str, category: FeatureCategory, options: LampParameters | None = None):
        super().__init__(name, category, options)
        self.state = options.get("state", False)
        self.brightness = options.get("brightness", 1)

    def execute(self, options: LampParameters | None = None):
        if options:
            if "state" in options and options["state"] is not None:
                self.state = bool(options.get("state", self.state))
                if self.options:
                    self.options["state"] = self.state
            if "brightness" in options and options["brightness"] is not None:
                self.brightness = int(options.get("brightness", self.brightness))
                if self.options:
                    self.options["brightness"] = self.brightness
        return json.dumps(self.to_dict())
    
    def get_status(self):
        return {"on": self.state, "brightness": self.brightness}

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state
        dict["brightness"] = self.brightness
        return dict
