import json

from . import Command
from shared import MQTTClient


class LockCommand(Command):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.state: bool | None = self.options.get("state")

    def execute(self):
        payload = json.dumps(self.to_dict())

        MQTTClient().publish(f"execution.{self.device_id}", payload)

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state

        return dict
