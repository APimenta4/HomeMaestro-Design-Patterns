import pickle
import json
from logging import getLogger

from automations import Automation
from devices import Device, Protocol

from . import MQTTClient, Singleton

logger = getLogger(__name__)


class HomeMaestro(metaclass=Singleton):
    def __init__(self):
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

        MQTTClient().subscribe(f"update.{device.id}")
        MQTTClient().subscribe(f"execution.{device.id}")

    def remove_device(self, id: int):
        device = self.get_device_by_id(id)
        if device is None:
            raise ValueError(f"Device with id '{id}' does not exist in HomeMaestro")

        self.connected_devices.discard(device)
        self.unconnected_devices.discard(device)

        MQTTClient().unsubscribe(f"update.{device.id}")
        MQTTClient().unsubscribe(f"execution.{device.id}")


    def add_automation(self, automation: Automation):
        self.automations.add(automation)

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
        logger.info(f"HomeMaestro received MQTT event on topic '{topic}' with payload '{payload}'")
        try:
            parts = topic.split(".")
            if len(parts) != 2:
                logger.warning("Received an MQTT event with an invalid topic format: %s", topic)
                return
            
            operation, device_id_str = parts
            device_id = int(device_id_str)

            if operation == "update":
                for automation in self.automations:
                    automation.attempt_automation(device_id, payload)
            elif operation == "execution":
                device = self.get_device_by_id(device_id)
                if device is None:
                    logger.warning("Received execution for unknown device id: %d", device_id)
                    return
                
                if device.status.value() != "online":
                    return
                
                data: dict[str, object] = json.loads(payload)
                device.execute_feature(data.get("feature_id"), data)
        except (ValueError, IndexError):
            logger.warning("Could not parse MQTT topic: %s", topic)

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
            MQTTClient().subscribe(f"update.{device.id}")
            MQTTClient().subscribe(f"execution.{device.id}")

        MQTTClient().set_event_handler(self._handle_mqtt_event)
