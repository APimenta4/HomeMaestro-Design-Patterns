import random

from . import Feature


class BlindsFeature(Feature):
    def __init__(self, name: str, options: dict[str, object] | None = None):
        super().__init__(name, options)
        self.position: float = 0.0  # fully open

    def execute(self):
        # Virtual device, therefore we simulate how much the blinds will be opened
        self.position = round(random.uniform(0.0, 1.0), 2)

    def get_status(self):
        return {"position": self.position}

    def to_dict(self):
        dict = super().to_dict()
        return dict
