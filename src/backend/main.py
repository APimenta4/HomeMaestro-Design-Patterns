from actions import ExternalAction
from actions.commands import LightsCommand
from devices import Device, DeviceStatus
from devices.features import LampFeature
from devices.hubs import ZWaveHub
from home_maestro.home_maestro import HomeMaestro
from integrations import TelegramIntegration, WhatsAppIntegration
from rules import AutomationRule
from triggers import TimeTrigger
from triggers.conditions import LightsCondition
from api import app

if __name__ == "__main__":

    # Sample devices
    features = set()
    features.add(LampFeature({"max_brightness": 100}))
    device1 = Device(DeviceStatus.ONLINE, features)
    device2 = Device(DeviceStatus.OFFLINE, features)
    hub = ZWaveHub({device1})

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
        devices={hub, device2},
        automation_rules={automation_rule1},
        integrations={integration1, integration2},
    )

    # Start the API
    app.run(debug=True)
