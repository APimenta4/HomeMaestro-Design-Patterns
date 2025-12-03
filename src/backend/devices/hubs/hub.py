from abc import ABC, abstractmethod

from devices import Device, DeviceStatus, Protocol
from shared import HomeMaestro

home_maestro = HomeMaestro()


# We chose inheritance for Hubs as it will be easier to implement protocol-specific implementations
# once we move on to real devices instead of only virtual ones
class Hub(Device, ABC):
    def __init__(
        self,
        name: str,
        status: type[DeviceStatus],
    ):
        super().__init__(name=name, status=status, protocol=Protocol.HUBLESS)
        self.devices = set()

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict.pop("features", None)
        dict.pop("protocol", None)
        dict["devices"] = [device.to_dict() for device in self.devices]
        return dict

    def link_device(self, device: Device):
        self.devices.add(device)
        home_maestro.unconnected_devices.discard(device)
        home_maestro.connected_devices.add(device)

    def unpair_device(self, device: Device):
        home_maestro.connected_devices.discard(device)
        home_maestro.unconnected_devices.add(device)
        self.devices.discard(device)

    @abstractmethod
    def discover_devices(self):
        pass
