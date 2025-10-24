from actions import Action
from triggers import Trigger


class AutomationRule:
    def __init__(self, trigger: Trigger, action: Action):
        self.trigger = trigger
        self.action = action
