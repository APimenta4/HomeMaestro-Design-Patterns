from . import (Feature, FeatureCategory, LampFeature, BlindsFeature,
               TemperatureFeature, LockFeature)


# DESIGN PATTERN: Simple Factory
class FeatureFactory:
    @staticmethod
    def create_feature(name: str, category: str, options: dict, type: str) -> Feature:
        try:
            feature_category = FeatureCategory(category.upper())
        except ValueError as exc:
            raise ValueError(f"The provided feature category is not supported: {category}") from exc
        match type.lower():
            case "lamp":
                return LampFeature(name=name, category=feature_category, options=options)
            case "blinds":
                return BlindsFeature(name=name, category=feature_category, options=options)
            case "temperature":
                return TemperatureFeature(name=name, category=feature_category, options=options)
            case "lock":
                return LockFeature(name=name, category=feature_category, options=options)
            case _:
                raise ValueError(f"The provided feature type is not supported: {type}")
