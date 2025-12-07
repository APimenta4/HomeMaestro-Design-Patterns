import pickle
from abc import ABC, abstractmethod


class Identifiable(ABC):
    _id_counter = 0  # Shared counter for unique IDs

    def __init__(self, name: str):
        self.id = self._assign_id()
        self.name = name

    @classmethod
    def _assign_id(cls) -> int:
        Identifiable._id_counter += 1
        return Identifiable._id_counter

    @classmethod
    def save_id_counter(cls, file_path: str):
        with open(file_path, "wb") as file:
            pickle.dump(cls._id_counter, file)

    @classmethod
    def load_id_counter(cls, file_path: str):
        with open(file_path, "rb") as file:
            cls._id_counter = pickle.load(file)

    @abstractmethod
    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
        }
