import os
from logging import getLogger

import paho.mqtt.client as mqtt

from . import Singleton

logger = getLogger(__name__)

BROKER_ENV = os.getenv("MQTT_BROKER", "localhost")


# DESIGN PATTERN: Publisher-Subscriber
class MQTTClient(metaclass=Singleton):
    def __init__(self, broker=BROKER_ENV, port=1883):
        self.client = mqtt.Client(clean_session=True)
        self.client.connect(broker, port, clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY)
        self.client.loop_start()
        self.event_handler = None
        self.client.on_message = self._on_event

    def set_event_handler(self, handler):
        self.event_handler = handler

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload, qos=2)

    def subscribe(self, topic: str):
        self.client.subscribe(topic, qos=2)

    def unsubscribe(self, topic: str):
        self.client.unsubscribe(topic)

    def _on_event(self, client, userdata, msg):
        # client and userData are unused but required by the MQTT callback signature
        if self.event_handler:
            self.event_handler(msg.topic, msg.payload.decode())
        else:
            logger.warning(
                "No event handler set for upcoming MQTT message on topic '%s'",
                msg.topic,
            )
