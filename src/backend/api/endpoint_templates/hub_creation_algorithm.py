import logging
from typing import Any

from devices import Device, DeviceStatusFactory
from devices.hubs import HubFactory
from shared import HomeMaestro

from . import EntityCreationAlgorithm

home_maestro = HomeMaestro()

logger = logging.getLogger(__name__)


class HubCreationAlgorithm(EntityCreationAlgorithm):

    def required_fields(self) -> dict[str, type]:
        return {"name": str, "status": str, "type": str}

    def optional_fields(self) -> dict[str, type]:
        return {}

    def prepare_input_data(self, payload: dict[str, Any]) -> dict[str, object]:
        payload["status"] = DeviceStatusFactory.create_status(payload["status"])
        return payload

    def instantiate_and_persist_entity(self, prepared_data: dict[str, Any]) -> Device:
        device = HubFactory.create_hub(**prepared_data)
        home_maestro.add_device(device)
        return device
