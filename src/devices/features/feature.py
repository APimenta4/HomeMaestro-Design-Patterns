from abc import ABC, abstractmethod


class Feature(ABC):
    def __init__(self, feature_options: dict[str, object]):
        self.feature_options = feature_options

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def get_status(self) -> None:
        pass
