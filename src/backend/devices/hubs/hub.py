from abc import ABC, abstractmethod

from devices import Device, DeviceStatus
from shared import append_type


class Hub(Device, ABC):
    def __init__(
        self, name: str, status: DeviceStatus, devices: set[Device] | None = None
    ):
        super().__init__(name=name, status=status, features=set())
        self.devices = devices or set()

    @append_type
    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["devices"] = [device.to_dict() for device in self.devices]
        dict.pop("features", None)
        return dict

    @abstractmethod
    def discover_devices(self):
        pass
