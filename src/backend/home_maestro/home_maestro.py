from automations import Automation
from shared import Singleton
from devices import Device
from notifications import NotificationService
from integrations import Integration


class HomeMaestro(metaclass=Singleton):
    def __init__(self, integrations: set[Integration] | None = None):
        self.notification_service = NotificationService(integrations or set())
        self.devices: set[Device] = set()
        self.automations: set[Automation] = set()

    def add_device(self, device: Device):
        self.devices.add(device)

    def add_automation(self, automation: Automation):
        self.automations.add(automation)
