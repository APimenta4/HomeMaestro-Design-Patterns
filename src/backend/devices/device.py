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

    # factory method
    @staticmethod
    def from_dict(data: dict[str, object]) -> "Device":
        name = data.get("name", "Unnamed Device")
        status_str = data.get("status", "offline").lower()
        status = (
            DeviceStatus[status_str]
            if status_str in DeviceStatus.__members__
            else DeviceStatus.OFFLINE
        )

        features_data = data.get("features", [])
        features = set()
        for feature_data in features_data:
            feature_type = feature_data.get("type")
            if feature_type == "LampFeature":
                features.add(LampFeature.from_dict(feature_data))
            # Add more feature types as needed

        return Device(name, status, features)
