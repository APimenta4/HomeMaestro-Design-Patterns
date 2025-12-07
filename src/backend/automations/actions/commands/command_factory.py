from . import (Command, BlindsCommand, LampCommand, LockCommand,
               TemperatureCommand)


# DESIGN PATTERN: Simple Factory
class CommandFactory:
    @staticmethod
    def create_command(type: str, device_id: int, feature_id: int, options: dict[str, object] | None = None) -> Command:
        match type.lower():
            case "lamp":
                return LampCommand(device_id=device_id, feature_id=feature_id, options=options)
            case "lock":
                return LockCommand(device_id=device_id, feature_id=feature_id, options=options)
            case "temperature":
                return TemperatureCommand(device_id=device_id, feature_id=feature_id, options=options)
            case "blinds":
                return BlindsCommand(device_id=device_id, feature_id=feature_id, options=options)
            case _:
                raise ValueError(f"The provided command type is not supported: {type}")
