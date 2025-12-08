from abc import ABC

from .messages import Message


class Integration(ABC):
    def __init__(self):
        self.sent_messages: list[Message] = []

    # Override method with integration-specific implementation
    # for the scope of this project, we will use a simple in-memory storage
    # considering we won't actually implement all integrations
    # once finished, this method (on the superclass) would be an abstractmethod
    def send_message(self, message: Message):
        self.sent_messages.append(message)

    def get_sent_messages(self) -> list[Message]:
        return self.sent_messages

    def to_dict(self) -> dict[str, object]:
        return {
            "type": self.__class__.__name__,
            "sent_messages": [message.to_dict() for message in self.sent_messages],
        }
