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

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["enabled"] = self.enabled
        dict["trigger"] = self.trigger.__class__.__name__
        dict["action"] = self.action.__class__.__name__
        dict["description"] = self.description
        return dict
