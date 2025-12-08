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
        # Validate that devices and features in conditions exist
        all_devices = home_maestro.get_all_devices()
        devices_map = {device.id: device for device in all_devices}

        for condition in payload["trigger"].conditions:
            if condition.device_id not in devices_map:
                raise ValueError(f"Device with id '{condition.device_id}' not found.")
            device = devices_map[condition.device_id]
            if not device.get_feature_by_id(condition.feature_id):
                raise ValueError(f"Feature with id '{condition.feature_id}' not found on device '{device.name}'.")
        payload["action"] = ActionFactory.create_action(**payload["action"])
        return payload

    def instantiate_and_persist_entity(
        self, prepared_data: dict[str, Any]
    ) -> Automation:
        automation = Automation(**prepared_data)
        home_maestro.add_automation(automation)
        return automation
