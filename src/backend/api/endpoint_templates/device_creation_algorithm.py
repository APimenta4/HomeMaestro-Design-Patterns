import logging
from typing import Any

from devices import Device, DeviceStatus
from devices.features import FeatureFactory
from devices.hubs import HubFactory
from shared import HomeMaestro

from . import EntityCreationAlgorithm

home_maestro = HomeMaestro()

logger = logging.getLogger(__name__)


class DeviceCreationAlgorithm(EntityCreationAlgorithm):

    def required_fields(self) -> dict[str, type]:
        return {"name": str, "status": str}

    def optional_fields(self) -> dict[str, type]:
        return {"type": str, "features": list}

    def prepare_input_data(self, payload: dict[str, Any]) -> dict[str, object]:
        if payload.get("type"):
            # TODO: Right now, hubs don't hold features, only other devices. This could be changed in the future.
            if payload.get("features"):
                logger.warning(
                    "Features were provided for new device of type Hub. These features will be ignored."
                )
                payload.pop("features")

        payload["status"] = DeviceStatus(payload["status"].lower())

        if payload.get("features"):
            payload["features"] = {
                FeatureFactory.create_feature(**feature)
                for feature in payload["features"]
            }

        return payload

    def instantiate_and_persist_entity(self, prepared_data: dict[str, Any]) -> Device:
        if prepared_data.get("type"):
            device = HubFactory.create_hub(**prepared_data)
        else:
            device = Device(**prepared_data)
        home_maestro.add_device(device)
        return device
