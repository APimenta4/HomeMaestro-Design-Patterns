from integrations import Integration
from integrations.messages import Message
from shared import Singleton


class NotificationService(metaclass=Singleton):
    def __init__(self, integrations: set[Integration]):
        self.integrations = integrations

    def add_integration(self, integration: Integration):
        self.integrations.add(integration)

    def get_integrations(self) -> set[Integration]:
        return self.integrations

    def send_notification_broadcast(self, message: Message):
        for integration in self.integrations:
            integration.send_message(message)
