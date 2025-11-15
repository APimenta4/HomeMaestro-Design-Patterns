from . import StateTrigger, ThresholdTrigger, TimeTrigger, Trigger
from .conditions import ConditionFactory


# DESIGN PATTERN: Simple Factory
class TriggerFactory:
    @staticmethod
    def create_trigger(type: str, conditions: list[dict]) -> Trigger:
        match type.lower():
            case "time":
                created_conditions = TriggerFactory.create_conditions(conditions)
                return TimeTrigger(conditions=created_conditions)
            case "threshold":
                created_conditions = TriggerFactory.create_conditions(conditions)
                return ThresholdTrigger(conditions=created_conditions)
            case "state":
                created_conditions = TriggerFactory.create_conditions(conditions)
                return StateTrigger(conditions=created_conditions)
            case _:
                raise ValueError(f"The provided trigger type is not supported: {type}")

    @staticmethod
    def create_conditions(conditions_data: list[dict]) -> set:
        conditions = set()
        for condition_data in conditions_data:
            condition = ConditionFactory.create_condition(**condition_data)
            conditions.add(condition)
        return conditions
