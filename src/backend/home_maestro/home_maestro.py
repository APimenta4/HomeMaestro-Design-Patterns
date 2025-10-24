from shared import Singleton
from devices import Device
from rules import AutomationRule
from notifications import NotificationService
from integrations import Integration


class HomeMaestro(metaclass=Singleton):
    def __init__(
        self,
        devices: set[Device],
        automation_rules: set[AutomationRule],
        integrations: set[Integration],
    ):
        self.notification_service = NotificationService(integrations)
        self.devices = devices
        self.automation_rules = automation_rules
