import json

from integrations.messages import MessageType
from shared import MQTTClient


class Notification:
    def __init__(self, type: str, content: str):
        self.type = MessageType(type)
        self.content = content

    def send(self):
        payload = json.dumps(self.to_dict())
        
        MQTTClient().publish(f"notification", payload)

    def to_dict(self) -> dict[str, object]:
        return {
            "type": self.type.value,
            "content": self.content,
        }
