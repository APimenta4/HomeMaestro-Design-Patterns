from . import Condition


class LockCondition(Condition):
    def __init__(self, device_id: int, feature_id: int):
        super().__init__(device_id, feature_id)

    def check(self):
        pass
