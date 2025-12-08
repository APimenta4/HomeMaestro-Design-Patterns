from integrations.messages import MessageType


class Notification:
    def __init__(self, type: str, content: str):
        self.type = MessageType(type)
        self.content = content

    def send(self):
        # TODO: Implement the actual sending logic (e.g., via WebSocket, email, etc.)
        print(f"Sending {self.type.value} notification: {self.content}")

    def to_dict(self) -> dict[str, object]:
        return {
            "type": self.type.value,
            "content": self.content,
        }
