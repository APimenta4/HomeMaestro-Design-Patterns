from devices import Device, DeviceStatus
from . import ZigbeeHub, ZWaveHub, TradfriHub, HueHub


# DESIGN PATTERN: Simple Factory
class HubFactory:
    @staticmethod
    def create_hub(
        name: str,
        status: DeviceStatus,
        type: str,
    ) -> Device:
        match type.lower():
            case "zigbee" | "zigbeehub":
                return ZigbeeHub(name=name, status=status)
            case "zwave" | "zwavehub":
                return ZWaveHub(name=name, status=status)
            case "tradfri" | "tradfrihub":
                return TradfriHub(name=name, status=status)
            case "hue" | "huehub":
                return HueHub(name=name, status=status)
            case _:
                raise ValueError(f"The provided hub type is not supported: {type}")
