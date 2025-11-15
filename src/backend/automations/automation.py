from shared import Identifiable

from .actions import Action
from .triggers import Trigger


class Automation(Identifiable):
    def __init__(
        self,
        name: str,
        trigger: Trigger,
        action: Action,
        enabled: bool = True,
        description: str | None = None,
    ):
        super().__init__(name)
        self.trigger = trigger
        self.action = action
        self.enabled = enabled
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "trigger": self.trigger.__class__.__name__,
            "action": self.action.__class__.__name__,
        }
