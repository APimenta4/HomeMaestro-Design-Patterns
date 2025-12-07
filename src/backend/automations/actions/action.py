from .commands import Command

from abc import ABC, abstractmethod




class Action(ABC):
    def __init__(self, commands: set[Command]):
        self.commands = commands

    @abstractmethod
    def invoke_executions(self):
        pass

    def to_dict(self) -> dict[str, object]:
        return {
            "commands": [command.__class__.__name__ for command in self.commands]
        }
    
    def to_dict_deep(self) -> dict[str, object]:
        return {
            "commands": [command.to_dict() for command in self.commands]
        }
