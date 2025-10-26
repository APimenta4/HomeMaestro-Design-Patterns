from abc import ABC, abstractmethod

from shared import Identifiable


class Feature(Identifiable, ABC):
    def __init__(self, name: str, options: dict[str, object] | None = None):
        super().__init__(name)
        self.options = options or {}

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["options"] = self.options
        return dict

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def get_status(self) -> None:
        pass
