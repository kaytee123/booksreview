import abc


class CommandRunner:
    def __init__(self):
        self.commands = {}

    def register(self, commands=[]):
        for command in commands:
            self.commands[command.name()] = command

        return self

    def execute(self, command_data, context={}):
        command = self.commands[command_data['name']]

        if command is None:
            return 'Error: can\'t find command'

        return command.handle(command_data, context)


# Command Interface
class Command(abc.ABC):

    """ Set name of command """
    @abc.abstractstaticmethod
    def name() -> str:
        pass

    """ Handle the command """
    @abc.abstractstaticmethod
    def handle(command={}, context={}) -> str:
        pass
