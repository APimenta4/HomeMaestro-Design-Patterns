from enum import Enum

from shared import Identifiable

from .features import Feature


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
        # self.state = ...     TODO: State Design Pattern

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["status"] = self.status.value
        dict["features"] = [feature.to_dict() for feature in self.features]
        return dict
