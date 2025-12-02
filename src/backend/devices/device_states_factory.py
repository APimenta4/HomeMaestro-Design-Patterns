from . import DeviceState, ErrorState, OfflineState, OnlineState


# DESIGN PATTERN: Simple Factory
class DeviceStateFactory:
    @staticmethod
    def create_state(state: str) -> type[DeviceState]:
        match state.lower():
            case "online":
                return OnlineState
            case "offline":
                return OfflineState
            case "error":
                return ErrorState
            case _:
                raise ValueError(f"The provided state type is not supported: {state}")
