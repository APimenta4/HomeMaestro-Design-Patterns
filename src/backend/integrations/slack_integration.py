from .messages import Message

from . import Integration


class SlackIntegration(Integration):
    def send_message(self, message: Message):
        pass
