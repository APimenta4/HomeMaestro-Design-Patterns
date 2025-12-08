from . import Condition


class LampCondition(Condition):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.state: bool | None = self.options.get("state")
        self.brightness: int | None = self.options.get("brightness")

    def check(self):
        pass

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state
        dict["brightness"] = self.brightness

        return dict
