from enum import Enum
from logging import getLogger

from shared import Identifiable, MQTTClient

from . import DeviceStatus
from .features import Feature

logger = getLogger(__name__)


class Protocol(Enum):
    HUBLESS = "HubLess"
    HUE = "Hue"
    ZWAVE = "ZWave"
    TRADFRI = "Tradfri"
    ZIGBEE = "Zigbee"


class Device(Identifiable):
    def __init__(
        self,
        name: str,
        status: type[DeviceStatus],
        protocol: Protocol,
        features: set[Feature] | None = None,
    ):
        super().__init__(name)
        self.status = status
        self.protocol = protocol
        self.features = features or set()

    def get_feature_by_id(self, feature_id: int) -> Feature | None:
        for feature in self.features:
            if feature.id == feature_id:
                return feature
        return None

    def execute_feature(
        self,
        feature_id: int,
        options: dict[str, object] | None = None,
    ):
        self.status.verify_can_execute()

        feature = self.get_feature_by_id(feature_id)
        if feature is None:
            raise ValueError(f"Feature with id '{feature_id}' does not exist on device")

        payload = feature.execute(options)
        MQTTClient().publish(f"{self.id}", payload)

    def get_feature_status(self, feature_id: int):
        self.status.verify_can_obtain_status()

        feature = self.get_feature_by_id(feature_id)
        if feature is None:
            raise ValueError(f"Feature with id '{feature_id}' does not exist on device")
        return feature.get_status()

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["status"] = self.status.value()
        dict["protocol"] = self.protocol.value
        dict["features"] = [feature.__class__.__name__ for feature in self.features]
        return dict

    def to_dict_deep(self) -> dict[str, object]:
        dict = self.to_dict()
        dict["features"] = [feature.to_dict() for feature in self.features]
        return dict
