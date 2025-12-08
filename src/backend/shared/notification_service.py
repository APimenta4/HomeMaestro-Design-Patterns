import pickle

from integrations import Integration
from integrations.messages import Message
from shared import Singleton


class NotificationService(metaclass=Singleton):
    def __init__(self):
        self.integrations = set()

    def add_integration(self, integration: Integration):
        self.integrations.add(integration)

    def get_integrations(self) -> set[Integration]:
        return self.integrations

    def send_notification_broadcast(self, message: Message):
        for integration in self.integrations:
            integration.send_message(message)

    def save_state(self, file_path: str):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    def load_state(self, file_path: str):
        with open(file_path, "rb") as file:
            loaded_instance = pickle.load(file)

        self.integrations = loaded_instance.integrations
