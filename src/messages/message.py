from enum import Enum
from dataclasses import dataclass


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
