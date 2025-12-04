from . import Feature
from typing import TypedDict

class LampParameters(TypedDict):
    state: bool
    brightness: int

class LampFeature(Feature):
    def __init__(self, name: str, options: LampParameters | None = None):
        super().__init__(name, options)
        self.state = options.get("state", False)
        self.brightness = options.get("brightness", 1)

    def execute(self):
        self.state = not self.state
    
    def get_status(self):
        return {"on": self.state, "brightness": self.brightness}

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state
        dict["brightness"] = self.brightness
        return dict
