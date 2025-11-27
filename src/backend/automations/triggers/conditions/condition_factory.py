from . import (
    BlindsCondition,
    Condition,
    LampCondition,
    LockCondition,
    TemperatureCondition,
)


# DESIGN PATTERN: Simple Factory
class ConditionFactory:
    @staticmethod
    def create_condition(type: str) -> Condition:
        match type.lower():
            case "blinds":
                return BlindsCondition()
            case "lock":
                return LockCondition()
            case "temperature":
                return TemperatureCondition()
            case "lamp":
                return LampCondition()
            case _:
                raise ValueError(
                    f"The provided condition type is not supported: {type}"
                )
