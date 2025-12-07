from logging import getLogger

from shared import Identifiable

from .actions import Action
from .triggers import Trigger

logger = getLogger(__name__)


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
    
    def to_dict_deep(self) -> dict[str, object]:
        dict = self.to_dict()

        dict["trigger"] = self.trigger.to_dict_deep()
        dict["action"] = self.action.to_dict_deep()

        return dict

    def attempt_automation(self, device_id: int, payload: str) -> bool:
        # TODO: remove
        logger.info("Attempting automation '%s' with payload: %s", self.name, payload)
        if not self.enabled:
            return False

        if self.trigger.check_conditions(device_id, payload):
            self.action.invoke_executions()
            return True

        return False
