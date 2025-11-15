from . import (BlindsCommand, Command, LightsCommand, LockCommand,
               TemperatureCommand)


# DESIGN PATTERN: Simple Factory
class CommandFactory:
    @staticmethod
    def create_command(type: str) -> Command:
        match type.lower():
            case "lights":
                return LightsCommand()
            case "lock":
                return LockCommand()
            case "temperature":
                return TemperatureCommand()
            case "blinds":
                return BlindsCommand()
            case _:
                raise ValueError(f"The provided command type is not supported: {type}")
