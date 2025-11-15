from automations import Automation
from devices import Device
from integrations import Integration
from notifications import NotificationService
from shared import Singleton


class HomeMaestro(metaclass=Singleton):
    def __init__(self, integrations: set[Integration] | None = None):
        self.notification_service = NotificationService(integrations or set())
        self.devices: set[Device] = set()
        self.automations: set[Automation] = set()

    def add_device(self, device: Device):
        self.devices.add(device)

    def add_automation(self, automation: Automation):
        self.automations.add(automation)

    def get_automation_by_id(self, automation_id: int) -> Automation | None:
        for automation in self.automations:
            if automation.id == automation_id:
                return automation
        return None
