from . import CommandAction, ExternalAction, NotificationAction, Action
from .commands import CommandFactory


# DESIGN PATTERN: Simple Factory
class ActionFactory:
    @staticmethod
    def create_action(type: str, commands: list[dict]) -> Action:
        match type.lower():
            case "command":
                created_commands = ActionFactory.create_commands(commands)
                return CommandAction(created_commands)
            case "external":
                created_commands = ActionFactory.create_commands(commands)
                return ExternalAction(created_commands)
            case "notification":
                created_commands = ActionFactory.create_commands(commands)
                return NotificationAction(created_commands)
            case _:
                raise ValueError(f"The provided action type is not supported: {type}")

    @staticmethod
    def create_commands(commands_data: list[dict]) -> set:
        commands = set()
        for command_data in commands_data:
            command = CommandFactory.create_command(**command_data)
            commands.add(command)
        return commands
