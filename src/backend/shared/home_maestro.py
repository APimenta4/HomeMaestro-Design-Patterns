import pickle
from logging import getLogger

from automations import Automation
from devices import Device, Protocol
from integrations import Integration

from . import MQTTClient, NotificationService, Singleton

logger = getLogger(__name__)


class HomeMaestro(metaclass=Singleton):
    def __init__(self, integrations: set[Integration] | None = None):
        self.notification_service = NotificationService(integrations or set())
        # hubless devices and hubs
        self.connected_devices: set[Device] = set()
        # other devices that require connection to a hub
        self.unconnected_devices: set[Device] = set()
        self.automations: set[Automation] = set()
        MQTTClient().set_event_handler(self._handle_mqtt_event)

    def get_all_devices(self) -> set[Device]:
        return self.connected_devices | self.unconnected_devices

    def add_device(self, device: Device):
        if device in self.connected_devices | self.unconnected_devices:
            raise ValueError(
                f"Device with id '{device.id}' already exists in HomeMaestro"
            )
        if device.protocol == Protocol.HUBLESS:
            self.connected_devices.add(device)
        else:
            self.unconnected_devices.add(device)

        MQTTClient().subscribe(f"{device.id}")

    def remove_device(self, id: int):
        device = self.get_device_by_id(id)
        if device is None:
            raise ValueError(f"Device with id '{id}' does not exist in HomeMaestro")

        self.connected_devices.discard(device)
        self.unconnected_devices.discard(device)

        MQTTClient().unsubscribe(f"{device.id}")

    def add_automation(self, automation: Automation):
        self.automations.add(automation)

    def add_integration(self, integration: Integration):
        for existing_integration in self.notification_service.integrations:
            if isinstance(integration, type(existing_integration)):
                raise ValueError(
                    f"An integration of type '{type(integration).__name__}' already exists."
                )
        self.notification_service.add_integration(integration)

    def get_automation_by_id(self, automation_id: int) -> Automation | None:
        for automation in self.automations:
            if automation.id == automation_id:
                return automation
        return None

    def get_device_by_id(self, device_id: int) -> Device | None:
        for device in self.get_all_devices():
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

    def save_state(self, file_path: str):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    def load_state(self, file_path: str):
        with open(file_path, "rb") as file:
            loaded_instance = pickle.load(file)

        self.connected_devices = loaded_instance.connected_devices
        self.unconnected_devices = loaded_instance.unconnected_devices
        self.automations = loaded_instance.automations

        for device in self.get_all_devices():
            MQTTClient().subscribe(f"{device.id}")

        MQTTClient().set_event_handler(self._handle_mqtt_event)
