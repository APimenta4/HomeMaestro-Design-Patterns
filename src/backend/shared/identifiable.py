from abc import ABC, abstractmethod


class Identifiable(ABC):
    _id_counter = 0  # Shared counter for unique IDs

    def __init__(self, name: str):
        self.id = self._assign_id()
        self.name = name

    @classmethod
    def _assign_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    @abstractmethod
    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
        }
