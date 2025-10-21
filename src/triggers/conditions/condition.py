from abc import ABC, abstractmethod


class Condition(ABC):
    @abstractmethod
    def check(self):
        pass
