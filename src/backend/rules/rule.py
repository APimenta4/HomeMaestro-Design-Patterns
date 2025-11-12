from actions import Action
from triggers import Trigger


class Rule:
    def __init__(self, trigger: Trigger, action: Action):
        self.trigger = trigger
        self.action = action
