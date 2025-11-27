from .messages import Message

from . import Integration


class WebhookIntegration(Integration):
    def send_message(self, message: Message):
        pass
