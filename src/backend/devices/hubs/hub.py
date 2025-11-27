from abc import ABC, abstractmethod

from devices import Device, DeviceStatus


class Hub(Device, ABC):
    def __init__(
        self, name: str, status: DeviceStatus, devices: set[Device] | None = None
    ):
        super().__init__(name=name, status=status)
        # TODO: remove once implemented. Hubs shouldnt initialize with devices. They should discover them.
        self.devices = devices or set()

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict.pop("features", None)
        dict["devices"] = [device.to_dict() for device in self.devices]
        return dict

    @abstractmethod
    def discover_devices(self):
        pass
