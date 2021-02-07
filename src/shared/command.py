import abc
from .result import Result, Error


class CommandRunner:
    def __init__(self):
        self.commands = {}

    def register(self, commands=[]):
        for command in commands:
            self.commands[command.name()] = command

        return self

    def execute(self, raw_command: dict, context={}):
        command_name = raw_command.get('name', None)
        if command_name is None:
            err = Error("Command name is required", "VALIDATION", raw_command)
            return Result.err(err)

        command = self.commands.get(command_name, None)
        if command is None:
            err = Error("Command is not found", "VALIDATION", raw_command)
            return Result.err(err)

        return command.handle(
            raw_command.get('data', {}),
            context
        )

    def execute_multiple(self, commands: dict, context={}):
        if len(commands) < 1:
            return "Error: Invalid Syntax"

        result = {}
        for cmd in commands:
            command_name: str = cmd.get('name')

            # Ingnore commands the "_"
            if command_name.startswith('_'):
                continue

            book_or_err: Result = self.execute(cmd, context)
            result[command_name] = book_or_err.match(
                lambda data: {'data': data, 'error': None},
                lambda err: {'data': None, 'error': err.to_dict()},
            )

        return result


# Command Interface
class Command(abc.ABC):

    """ Set name of command """
    @abc.abstractstaticmethod
    def name() -> str:
        pass

    """ Handle the command """
    @abc.abstractstaticmethod
    def handle(raw_command: dict, context: dict) -> Result:
        pass
