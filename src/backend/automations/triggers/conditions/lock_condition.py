from . import Condition


class LockCondition(Condition):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.state: bool | None = self.options.get("state")


    def check(self):
        pass

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state

        return dict
