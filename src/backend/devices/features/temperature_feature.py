import random

from . import Feature


class TemperatureFeature(Feature):
    def __init__(self, name: str, options: dict[str, object] | None = None):
        super().__init__(name, options)
        self.temperature: int = 0

    def execute(self):
        # Virtual device, therefore we simulate temperature reading
        self.temperature = round(random.uniform(15.0, 25.0))

    def get_status(self):
        return {"temperature": self.temperature}

    def to_dict(self):
        dict = super().to_dict()
        return dict
