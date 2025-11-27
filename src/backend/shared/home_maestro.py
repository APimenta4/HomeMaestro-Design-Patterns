from logging import getLogger

from automations import Automation
from devices import Device
from integrations import Integration

from . import MQTTClient, NotificationService, Singleton

logger = getLogger(__name__)


class HomeMaestro(metaclass=Singleton):
    def __init__(self, integrations: set[Integration] | None = None):
        self.notification_service = NotificationService(integrations or set())
        self.devices: set[Device] = set()
        self.automations: set[Automation] = set()
        MQTTClient().set_event_handler(self._handle_mqtt_event)

    def add_device(self, device: Device):
        self.devices.add(device)
        MQTTClient().subscribe(f"{device.id}")

    def add_automation(self, automation: Automation):
        self.automations.add(automation)

    def get_automation_by_id(self, automation_id: int) -> Automation | None:
        for automation in self.automations:
            if automation.id == automation_id:
                return automation
        return None

    def get_device_by_id(self, device_id: int) -> Device | None:
        for device in self.devices:
            if device.id == device_id:
                return device
        return None

    def _handle_mqtt_event(self, topic: str, payload: str):
        try:
            device_id = int(topic)
            for automation in self.automations:
                if automation.device_id == device_id:
                    automation.attempt_automation(payload)
        except ValueError:
            logger.warning("Received an MQTT event with an invalid topic: %s", topic)
