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
    def create_condition(type: str, device_id: int, feature_id: int, options: dict[str, object] | None = None) -> Condition:
        match type.lower():
            case "blinds":
                return BlindsCondition(device_id=device_id, feature_id=feature_id, options=options)
            case "lock":
                return LockCondition(device_id=device_id, feature_id=feature_id, options=options)
            case "temperature":
                return TemperatureCondition(device_id=device_id, feature_id=feature_id, options=options)
            case "lamp":
                return LampCondition(device_id=device_id, feature_id=feature_id, options=options)
            case _:
                raise ValueError(
                    f"The provided condition type is not supported: {type}"
                )
