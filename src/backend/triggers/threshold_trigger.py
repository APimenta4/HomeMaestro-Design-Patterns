from . import Trigger


class ThresholdTrigger(Trigger):
    def check_conditions(self) -> bool:
        return True
