from actions import ExternalAction
from actions.commands import LightsCommand
from devices import Device, DeviceStatus
from devices.features import LampFeature
from devices.hubs import ZWaveHub, ZigbeeHub
from home_maestro.home_maestro import HomeMaestro
from integrations import TelegramIntegration, WhatsAppIntegration
from rules import AutomationRule
from triggers import TimeTrigger
from triggers.conditions import LightsCondition
from api.api import app


if __name__ == "__main__":

    # Sample devices
    features = set()
    features.add(LampFeature("My Dream Feature", {"max_brightness": 100}))
    features.add(
        LampFeature("Second Feature", {"second feature": "amazing capabilities"})
    )
    device1 = Device("Smartwatch", DeviceStatus.ONLINE, features)
    device2 = Device("Digital Clock 2018", DeviceStatus.OFFLINE, features)
    feature1 = LampFeature("Feature 1", {"something": "my test value"})
    feature2 = LampFeature("Feature 2", {"something else": "20"})
    feature3 = LampFeature("Feature 3", {"ADS feature": "10"})
    device3 = Device(
        "Test Device", DeviceStatus.OFFLINE, {feature1, feature2, feature3}
    )
    device4 = Device("Another Device", DeviceStatus.ERROR)
    device5 = Device("Simple Device", DeviceStatus.ONLINE, {feature2})
    hub = ZWaveHub("My first hub", DeviceStatus.ONLINE, {device1})
    hub2 = ZigbeeHub("ZigBee Hub", DeviceStatus.ONLINE, {device1})

    # Sample integrations
    integration1 = WhatsAppIntegration()
    integration2 = TelegramIntegration()

    # Sample automation rules
    condition1 = LightsCondition()
    command1 = LightsCommand()
    trigger1 = TimeTrigger({condition1})
    action1 = ExternalAction({command1})
    automation_rule1 = AutomationRule(trigger=trigger1, action=action1)

    home_maestro = HomeMaestro(
        integrations={integration1, integration2},
    )

    home_maestro.add_device(hub)
    home_maestro.add_device(hub2)
    home_maestro.add_device(device2)
    home_maestro.add_device(device3)
    home_maestro.add_device(device4)
    home_maestro.add_device(device5)

    home_maestro.add_automation_rule(automation_rule1)

    # Start the API
    app.run(debug=True)
