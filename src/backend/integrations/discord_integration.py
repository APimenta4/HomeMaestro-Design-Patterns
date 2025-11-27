from .messages import Message

from . import Integration


class DiscordIntegration(Integration):
    def send_message(self, message: Message):
        pass
