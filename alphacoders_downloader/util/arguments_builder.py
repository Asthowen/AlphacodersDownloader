from alphacoders_downloader.util.utils import print_error
import asyncio
import sys


class ArgumentsBuilder:
    def __init__(self, description: str, command_base: str, args: list = None):
        if args is None:
            args = sys.argv

        self.description = description
        self.command_base = command_base
        self.args = args

        self.arguments = {}
        self.__help_content = None

    def add_argument(
            self, argument_name: str, action=None, description: str = None, command_usage: str = None
    ):
        self.arguments[argument_name.lower()] = {
            'action': action, 'description': description, 'command_usage': command_usage
        }

    def build_help(self):
        if self.__help_content is None:
            self.__help_content = f"\n\033[1m{self.description}\033[0m\n\nCommand list:\n"
            for _, command_json in self.arguments.items():
                self.__help_content += f'・\033[1m{self.command_base} {command_json["command_usage"]}\033[' \
                                       f'0m | {command_json["description"]}\n'

        print(self.__help_content)

    async def build(self):
        if len(self.args) == 1 or '--help' in self.args or '-h' in self.args:
            return self.build_help()

        has_been_found = False

        for argument in self.args:
            argument = argument.lower()
            if argument in self.arguments:
                has_been_found = True
                self.arguments[argument]['args'] = self.args
                if asyncio.iscoroutinefunction(self.arguments[argument]['action']):
                    await self.arguments[argument]['action'](self.arguments[argument])
                else:
                    self.arguments[argument]['action'](self.arguments[argument])
        if has_been_found is False:
            print_error(f"\033[1mThis command doesn't exist. Please check the command: {self.command_base} -H.\033[0m")
