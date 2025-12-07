from . import Condition


class BlindsCondition(Condition):
    def __init__(self, device_id: int, feature_id: int):
        super().__init__(device_id, feature_id)

    def check(self):
        pass
