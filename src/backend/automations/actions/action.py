from abc import ABC, abstractmethod
from .commands import Command


class Action(ABC):
    def __init__(self, commands: set[Command]):
        self.commands = commands

    @abstractmethod
    def invoke_executions(self):
        pass
