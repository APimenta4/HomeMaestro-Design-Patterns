from . import DeviceStatus, ErrorStatus, OfflineStatus, OnlineStatus


# DESIGN PATTERN: Simple Factory
class DeviceStatusFactory:
    @staticmethod
    def create_status(state: str) -> type[DeviceStatus]:
        match state.lower():
            case "online":
                return OnlineStatus
            case "offline":
                return OfflineStatus
            case "error":
                return ErrorStatus
            case _:
                raise ValueError(f"The provided status type is not supported: {state}")
