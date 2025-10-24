from abc import ABC, abstractmethod
from messages import Message


class Integration(ABC):
    @abstractmethod
    def send_message(self, message: Message):
        pass
