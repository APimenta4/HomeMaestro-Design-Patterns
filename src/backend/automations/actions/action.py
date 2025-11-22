from .commands import Command

from abc import ABC, abstractmethod




class Action(ABC):
    def __init__(self, commands: set[Command]):
        self.commands = commands

    @abstractmethod
    def invoke_executions(self):
        pass
