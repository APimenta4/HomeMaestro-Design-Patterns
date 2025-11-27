from . import Trigger


class TimeTrigger(Trigger):
    def check_conditions(self, *args, **kwargs) -> bool:
        return True
