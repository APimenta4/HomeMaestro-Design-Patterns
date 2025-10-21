from messages import Message

from . import Integration


class WhatsAppIntegration(Integration):
    def send_message(self, message: Message):
        pass
