from . import Trigger


class TimeTrigger(Trigger):
    def check_conditions(self) -> bool:
        return True
