from messages import Message

from . import Integration


class TelegramIntegration(Integration):
    def send_message(self, message: Message):
        pass
