import logging
from typing import Any

from devices import Device, DeviceStatusFactory, Protocol
from devices.features import FeatureFactory
from shared import HomeMaestro

from . import EntityCreationAlgorithm

home_maestro = HomeMaestro()

logger = logging.getLogger(__name__)


class DeviceCreationAlgorithm(EntityCreationAlgorithm):

    def required_fields(self) -> dict[str, type]:
        return {"name": str, "status": str, "protocol": str}

    def optional_fields(self) -> dict[str, type]:
        return {"features": list}

    def prepare_input_data(self, payload: dict[str, Any]) -> dict[str, object]:
        try:
            payload["protocol"] = Protocol(payload["protocol"])
        except ValueError as exc:
            raise ValueError(
                f"The provided protocol type is not supported: {payload['protocol']}"
            ) from exc

        payload["status"] = DeviceStatusFactory.create_status(payload["status"])

        if payload.get("features"):
            payload["features"] = {
                FeatureFactory.create_feature(**feature)
                for feature in payload["features"]
            }

        return payload

    def instantiate_and_persist_entity(self, prepared_data: dict[str, Any]) -> Device:
        device = Device(**prepared_data)
        home_maestro.add_device(device)
        return device
