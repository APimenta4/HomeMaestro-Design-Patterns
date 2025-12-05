from abc import ABC, abstractmethod

from .messages import Message


class Integration(ABC):
    def __init__(self):
        self.sent_messages: list[Message] = []

    # In a real implementation, this method would interface with the Integration API (WhatsApp, etc.),
    # so it would have a more complex and specific implementation in each child class.
    # Since this is a mock implementation for testing purposes and we simply store the messages, 
    # the implementation is the same for all child classes.
    def send_message(self, message: Message):
        self.sent_messages.append(message)

    def get_sent_messages(self) -> list[Message]:
        return self.sent_messages
    
    def to_dict(self) -> dict[str, object]:
        return {
            "type": self.__class__.__name__,
            "sent_messages": [message.to_dict() for message in self.sent_messages],
        }
