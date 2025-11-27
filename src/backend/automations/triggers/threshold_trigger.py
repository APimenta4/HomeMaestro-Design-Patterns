from . import Trigger


class ThresholdTrigger(Trigger):
    def check_conditions(self, *args, **kwargs) -> bool:
        return True
