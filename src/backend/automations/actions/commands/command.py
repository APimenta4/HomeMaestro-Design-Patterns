from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def to_dict(self) -> dict[str, object]:
        return {
            # Add command attributes here if needed
        }
