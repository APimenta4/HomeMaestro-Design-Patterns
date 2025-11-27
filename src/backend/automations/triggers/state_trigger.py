from . import Trigger


class StateTrigger(Trigger):
    def check_conditions(self, *args, **kwargs) -> bool:
        return True
