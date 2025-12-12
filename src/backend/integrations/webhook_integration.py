from logging import getLogger

import requests

from . import Integration
from .messages import Message

logger = getLogger(__name__)


class WebhookIntegration(Integration):
    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def send_message(self, message: Message):
        try:
            response = requests.post(
                self.webhook_url, json=message.to_dict(), timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to send message to webhook: %s", e)

        self.sent_messages.append(message)
