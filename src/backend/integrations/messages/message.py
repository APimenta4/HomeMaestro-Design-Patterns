from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    ALERT = "alert"
    STATUS_UPDATE = "status_update"
    DEVICE_EVENT = "device_event"
    AUTOMATION_RESULT = "automation_result"
    ERROR = "error"


@dataclass
class Message:
    message_type: MessageType
    content: str
    timestamp: str

    def to_dict(self) -> dict[str, object]:
        return {
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp,
        }
