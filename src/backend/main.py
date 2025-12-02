import logging

from api import app
from automations import Automation
from automations.actions import ExternalAction
from automations.actions.commands import LampCommand
from automations.triggers import TimeTrigger
from automations.triggers.conditions import LampCondition
from devices import Device, DeviceState, ErrorState, OfflineState, OnlineState
from devices.features import Feature, LampFeature
from devices.hubs import ZigbeeHub, ZWaveHub
from integrations import TelegramIntegration, WhatsAppIntegration
from shared import HomeMaestro, MQTTClient

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

    # Sample devices
    features: set[Feature] = set()
    features.add(LampFeature("My Dream Feature", {"max_brightness": 100}))
    features.add(
        LampFeature("Second Feature", {"second feature": "amazing capabilities"})
    )
    device1 = Device("Smartwatch", OnlineState, features)
    device2 = Device("Digital Clock 2018", OfflineState, features)
    feature1 = LampFeature("Feature 1", {"something": "my test value"})
    feature2 = LampFeature("Feature 2", {"something else": "20"})
    feature3 = LampFeature("Feature 3", {"ADS feature": "10"})
    device3 = Device("Test Device", OfflineState, {feature1, feature2, feature3})
    device4 = Device("Another Device", ErrorState)
    device5 = Device("Simple Device", OnlineState, {feature2})
    hub = ZWaveHub("My first hub", OnlineState, {device1})
    hub2 = ZigbeeHub("ZigBee Hub", OnlineState, {device1})

    # Sample integrations
    integration1 = WhatsAppIntegration()
    integration2 = TelegramIntegration()

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
    )

    home_maestro = HomeMaestro(integrations={integration1, integration2})
    MQTTClient()

    # Adicionar devices
    home_maestro.add_device(hub)
    home_maestro.add_device(hub2)
    home_maestro.add_device(device1)
    home_maestro.add_device(device2)
    home_maestro.add_device(device3)
    home_maestro.add_device(device4)
    home_maestro.add_device(device5)

    # Adicionar automações
    home_maestro.add_automation(automation1)
    home_maestro.add_automation(automation2)

    # Start the API
    app.run(debug=True, use_reloader=False)
