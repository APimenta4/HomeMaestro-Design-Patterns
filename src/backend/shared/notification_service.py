from integrations import Integration
from integrations.messages import Message
from shared import Singleton


class NotificationService(metaclass=Singleton):
    def __init__(self, integrations: set[Integration]):
        self.integrations = integrations

    def send_notification(self, message: Message):
        pass
