import json

from . import Command
from shared import MQTTClient


class BlindsCommand(Command):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.position: int | None = self.options.get("position")

    def execute(self):
        payload = json.dumps(self.to_dict())

        MQTTClient().publish(f"execution.{self.device_id}", payload)

    def to_dict(self):
        dict = super().to_dict()
        dict["position"] = self.position

        return dict
