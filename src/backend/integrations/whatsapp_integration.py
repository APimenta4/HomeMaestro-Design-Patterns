from .messages import Message

from . import Integration


class WhatsAppIntegration(Integration):
    def __init__(self):
        self.sent_messages: list[Message] = []

    def send_message(self, message: Message):
        self.sent_messages.append(message)

    def get_sent_messages(self) -> list[Message]:
        return self.sent_messages
