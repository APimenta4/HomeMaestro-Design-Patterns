from . import Trigger


class StateTrigger(Trigger):
    def check_conditions(self) -> bool:
        return True
