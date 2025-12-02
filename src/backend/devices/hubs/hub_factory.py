from devices import Device, DeviceState
from devices.hubs import HueHub, TradfriHub, ZigbeeHub, ZWaveHub


# DESIGN PATTERN: Simple Factory
class HubFactory:
    @classmethod
    def create_hub(
        cls,
        name: str,
        state: type[DeviceState],
        type: str,
    ) -> Device:
        match type.lower():
            case "zigbee" | "zigbeehub":
                return ZigbeeHub(name=name, state=state)
            case "zwave" | "zwavehub":
                return ZWaveHub(name=name, state=state)
            case "tradfri" | "tradfrihub":
                return TradfriHub(name=name, state=state)
            case "hue" | "huehub":
                return HueHub(name=name, state=state)
            case _:
                raise ValueError(f"The provided hub type is not supported: {type}")
