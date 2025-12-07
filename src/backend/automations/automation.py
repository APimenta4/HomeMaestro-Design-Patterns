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
        device_id: int,
        enabled: bool = True,
        description: str | None = None,
    ):
        super().__init__(name)
        self.trigger = trigger
        self.action = action
        # Here we use device_id instead of device to mimick an event driven architecture,
        # where the automation wouldn't normally be able to hold a direct reference to the device.
        # ------------------------
        self.device_id = device_id
        # ------------------------
        self.enabled = enabled
        self.description = description

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["enabled"] = self.enabled
        dict["trigger"] = self.trigger.__class__.__name__
        dict["action"] = self.action.__class__.__name__
        dict["device_id"] = self.device_id
        dict["description"] = self.description
        return dict
    
    def to_dict_deep(self) -> dict[str, object]:
        dict = self.to_dict()
        # The trigger and action objects in an automation already hold all their necessary data,
        # so we can convert them to dictionaries directly.
        # If they had complex objects, we would need to implement `to_dict` in them as well.
        # dict["trigger"] = self.trigger.__dict__
        # dict["action"] = self.action.__dict__
        return dict

    def attempt_automation(self, payload: str) -> bool:
        # TODO: remove
        logger.info("Attempting automation '%s' with payload: %s", self.name, payload)
        if not self.enabled:
            return False

        if self.trigger.check_conditions(payload):
            self.action.invoke_executions()
            return True

        return False
