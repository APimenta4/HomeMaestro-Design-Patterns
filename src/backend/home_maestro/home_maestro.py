from shared import Singleton
from devices import Device
from rules import AutomationRule
from notifications import NotificationService
from integrations import Integration


class HomeMaestro(metaclass=Singleton):
    def __init__(
        self,
        integrations: set[Integration] | None = None,
    ):
        self.notification_service = NotificationService(integrations or set())
        self.devices: set[Device] = set()
        self.automation_rules: set[AutomationRule] = set()

    def add_device(self, device: Device):
        self.devices.add(device)

    def add_automation_rule(self, rule: AutomationRule):
        self.automation_rules.add(rule)
