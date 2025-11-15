from . import Feature, LampFeature


# DESIGN PATTERN: Simple Factory
class FeatureFactory:
    @staticmethod
    def create_feature(name: str, options: dict, type: str) -> Feature:
        match type.lower():
            case "lamp":
                return LampFeature(name=name, options=options)
            case _:
                raise ValueError(f"The provided feature type is not supported: {type}")
