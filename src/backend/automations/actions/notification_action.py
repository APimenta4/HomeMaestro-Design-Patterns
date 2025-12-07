# notification_action.py
from .action import Action  # Importa diretamente de action.py
from .notifications import Notification


class NotificationAction(Action):
    def __init__(self, notifications: set[Notification]):
        self.notifications = notifications
    
    def invoke_executions(self):
        pass

    def to_dict(self) -> dict[str, object]:
        return {
            "notifications": [notification.__class__.__name__ for notification in self.notifications]
        }
    
    def to_dict_deep(self) -> dict[str, object]:
        return {
            "notifications": [notification.to_dict() for notification in self.notifications]
        }