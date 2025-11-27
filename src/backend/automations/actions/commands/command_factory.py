from . import (Command, BlindsCommand, LampCommand, LockCommand,
               TemperatureCommand)


# DESIGN PATTERN: Simple Factory
class CommandFactory:
    @staticmethod
    def create_command(type: str) -> Command:
        match type.lower():
            case "lamp":
                return LampCommand()
            case "lock":
                return LockCommand()
            case "temperature":
                return TemperatureCommand()
            case "blinds":
                return BlindsCommand()
            case _:
                raise ValueError(f"The provided command type is not supported: {type}")
