from enum import Enum
from devices.features import Feature

from shared import append_type, Identifiable


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


class Device(Identifiable):
    def __init__(
        self, name: str, status: DeviceStatus, features: set[Feature] | None = None
    ):
        super().__init__(name)
        self.status = status
        self.features = features or set()

    @append_type
    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["status"] = self.status.value
        dict["features"] = [feature.to_dict() for feature in self.features]
        return dict
