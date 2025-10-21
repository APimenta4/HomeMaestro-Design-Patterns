from enum import Enum
from devices.features import Feature


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


class Device:
    def __init__(self, status: DeviceStatus, features: set[Feature]):
        self.status = status
        self.features = features
