from typing import Any

from automations import Automation
from automations.actions import ActionFactory
from automations.triggers import TriggerFactory
from shared import HomeMaestro

from . import EntityCreationAlgorithm

home_maestro = HomeMaestro()


class AutomationCreationAlgorithm(EntityCreationAlgorithm):

    def required_fields(self) -> dict[str, type]:
        return {"name": str, "trigger": dict, "action": dict}

    def optional_fields(self) -> dict[str, type]:
        return {"description": str, "enabled": bool}

    def prepare_input_data(self, payload: dict[str, Any]) -> dict[str, object]:
        payload["trigger"] = TriggerFactory.create_trigger(**payload["trigger"])
        payload["action"] = ActionFactory.create_action(**payload["action"])
        return payload

    def instantiate_and_persist_entity(
        self, prepared_data: dict[str, Any]
    ) -> Automation:
        automation = Automation(**prepared_data)
        home_maestro.add_automation(automation)
        return automation
