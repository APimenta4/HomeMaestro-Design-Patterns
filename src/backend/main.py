import logging

from api import app
from automations import Automation
from automations.actions import ExternalAction
from automations.actions.commands import LampCommand
from automations.triggers import TimeTrigger
from automations.triggers.conditions import LampCondition
from devices import Device, ErrorStatus, OfflineStatus, OnlineStatus, Protocol
from devices.features import Feature, LampFeature
from devices.hubs import ZigbeeHub, ZWaveHub
from integrations import TelegramIntegration, WhatsAppIntegration
from shared import HomeMaestro

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

    home_maestro = HomeMaestro(
        integrations={WhatsAppIntegration(), TelegramIntegration()}
    )

    # Sample devices
    features: set[Feature] = set()
    features.add(LampFeature("My Dream Feature", {"max_brightness": 100}))
    features.add(
        LampFeature("Second Feature", {"second feature": "amazing capabilities"})
    )
    device1 = Device("Smartwatch", OnlineStatus, Protocol.HUBLESS, features)
    device2 = Device("Digital Clock 2018", OfflineStatus, Protocol.TRADFRI, features)
    feature1 = LampFeature("Feature 1", {"something": "my test value"})
    feature2 = LampFeature("Feature 2", {"something else": "20"})
    feature3 = LampFeature("Feature 3", {"ADS feature": "10"})
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

    # home_maestro.add_device(hub)
    # home_maestro.add_device(hub2)
    # home_maestro.add_device(device1)
    # home_maestro.add_device(device2)
    # home_maestro.add_device(device3)
    # home_maestro.add_device(device4)
    # home_maestro.add_device(device5)
    # home_maestro.add_device(device6)
    # home_maestro.add_device(device7)
    # home_maestro.add_device(device8)
    # home_maestro.add_device(device9)
    # home_maestro.add_device(device10)
    # home_maestro.add_device(device11)
    # home_maestro.add_device(device12)

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

    # Start the API
    app.run(debug=True, use_reloader=False)
