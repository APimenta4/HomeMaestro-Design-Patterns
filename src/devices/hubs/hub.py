from abc import ABC, abstractmethod

from devices import Device


class Hub(ABC, Device):
    def __init__(self, devices: set[Device]):
        self.devices = devices

    @abstractmethod
    def discover_devices(self):
        pass
