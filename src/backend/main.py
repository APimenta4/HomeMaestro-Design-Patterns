import atexit
import logging
import os
from datetime import datetime

from api import app
from automations import Automation
from automations.actions import ExternalAction
from automations.actions.commands import LampCommand
from automations.triggers import TimeTrigger
from automations.triggers.conditions import LampCondition
from devices import Device, ErrorStatus, OfflineStatus, OnlineStatus, Protocol
from devices.features import (
    BlindsFeature,
    Feature,
    FeatureFactory,
    LampFeature,
    TemperatureFeature,
)
from devices.hubs import ZigbeeHub, ZWaveHub
from integrations import (
    DiscordIntegration,
    SlackIntegration,
    TelegramIntegration,
    WebhookIntegration,
    WhatsAppIntegration,
)
from integrations.messages import Message, MessageType
from shared import HomeMaestro, Identifiable

logging.basicConfig(level=logging.DEBUG)

STATE_FILE = "home_maestro_state.pkl"
ID_COUNTER_FILE = "id_counter.pkl"


def create_sample_data():
    home_maestro = HomeMaestro()

    # Sample devices
    features: set[Feature] = set()
    features.add(
        FeatureFactory.create_feature(
            "Luzes", "ACTUATOR", {"state": True, "brightness": 5}, "lamp"
        )
    )
    features.add(
        FeatureFactory.create_feature("Cortinas", "ACTUATOR", {"position": 0}, "blinds")
    )
    features.add(
        FeatureFactory.create_feature(
            "Termometro", "SENSOR", {"temperature": 25}, "temperature"
        )
    )

    device1 = Device("Test Device", OnlineStatus, Protocol.HUBLESS, features)
    device2 = Device("Digital Clock 2018", OfflineStatus, Protocol.TRADFRI, features)
    feature1 = FeatureFactory.create_feature(
        "Feature 1", "ACTUATOR", {"something": "my test value"}, "lamp"
    )
    feature2 = FeatureFactory.create_feature(
        "Feature 2", "ACTUATOR", {"something else": "20"}, "lamp"
    )
    feature3 = FeatureFactory.create_feature(
        "Feature 3", "ACTUATOR", {"ADS feature": "10"}, "lamp"
    )
    device3 = Device(
        "Test Device", OfflineStatus, Protocol.ZWAVE, {feature1, feature2, feature3}
    )
    device4 = Device("Another Device", ErrorStatus, Protocol.ZIGBEE)
    device5 = Device("Simple Device", OnlineStatus, Protocol.ZIGBEE, {feature2})
    device6 = Device("Extra Device", OnlineStatus, Protocol.ZIGBEE, {feature3})
    device7 = Device("Cool Device", OfflineStatus, Protocol.ZWAVE, {feature1})
    device8 = Device("Interesting Device", ErrorStatus, Protocol.TRADFRI, {feature1})
    device9 = Device("Hubless Device", OnlineStatus, Protocol.HUBLESS, features)
    device10 = Device("Zigbee Device", OnlineStatus, Protocol.ZIGBEE, features)
    device11 = Device("Another Hubless Device", OfflineStatus, Protocol.HUBLESS)
    device12 = Device("Another Zigbee Device", OfflineStatus, Protocol.ZIGBEE)
    device12 = Device("Wonderful Device", OfflineStatus, Protocol.HUBLESS)
    hub = ZWaveHub("My first hub", OnlineStatus)
    hub2 = ZigbeeHub("ZigBee Hub", OnlineStatus)

    home_maestro.add_device(hub)
    home_maestro.add_device(hub2)
    home_maestro.add_device(device1)
    home_maestro.add_device(device2)
    home_maestro.add_device(device3)
    home_maestro.add_device(device4)
    home_maestro.add_device(device5)
    home_maestro.add_device(device6)
    home_maestro.add_device(device7)
    home_maestro.add_device(device8)
    home_maestro.add_device(device9)
    home_maestro.add_device(device10)
    home_maestro.add_device(device11)
    home_maestro.add_device(device12)

    home_maestro.add_integration(WhatsAppIntegration())
    home_maestro.add_integration(TelegramIntegration())
    home_maestro.add_integration(DiscordIntegration())
    home_maestro.add_integration(SlackIntegration())
    home_maestro.add_integration(WebhookIntegration())

    # Sample notification
    alert_message = Message(
        message_type=MessageType.ALERT,
        content="The front door was left open.",
        timestamp=datetime.now().isoformat(),
    )

    home_maestro.notification_service.send_notification_broadcast(alert_message)

    # Sample automations
    condition1 = LampCondition()
    command1 = LampCommand()
    trigger1 = TimeTrigger({condition1})
    action1 = ExternalAction({command1})
    automation1 = Automation(
        name="my beautiful automation",
        trigger=trigger1,
        action=action1,
        description="just testing",
        device_id=1,
    )
    automation2 = Automation(
        name="another automation",
        trigger=trigger1,
        action=action1,
        device_id=2,
        enabled=False,
    )

    home_maestro.add_automation(automation1)
    home_maestro.add_automation(automation2)

    # Sample automations
    condition1 = LampCondition()
    command1 = LampCommand()
    trigger1 = TimeTrigger({condition1})


def save_state():
    logging.info("Saving application state")
    HomeMaestro().save_state(STATE_FILE)
    Identifiable.save_id_counter(ID_COUNTER_FILE)


if __name__ == "__main__":
    # Register shutdown handler
    atexit.register(save_state)

    if os.path.exists(STATE_FILE) and os.path.exists(ID_COUNTER_FILE):
        logging.info("Loading saved state")
        Identifiable.load_id_counter(ID_COUNTER_FILE)
        HomeMaestro().load_state(STATE_FILE)
    else:
        logging.info("No saved state found. Creating new instance sample data")
        create_sample_data()

    # Start the API
    app.run(debug=True, use_reloader=False)
