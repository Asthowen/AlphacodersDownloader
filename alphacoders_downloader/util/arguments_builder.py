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
            for x in self.arguments:
                self.__help_content += f'・\033[1m{self.command_base} {self.arguments[x]["command_usage"]}\033[0m ' \
                                       f'| {self.arguments[x]["description"]}\n'

        print(self.__help_content)

    async def build(self):
        if len(self.args) == 1 or '--help' in self.args or '-h' in self.args:
            return self.build_help()

        has_been_found = False

        for i, x in enumerate(self.args):
            x = x.lower()
            if x in self.arguments:
                has_been_found = True
                self.arguments[x]['args'] = self.args
                if asyncio.iscoroutinefunction(self.arguments[x]['action']):
                    await self.arguments[x]['action'](self.arguments[x])
                else:
                    self.arguments[x]['action'](self.arguments[x])
        if has_been_found is False:
            print_error(f"\033[1mThis command doesn't exist. Please check the command: {self.command_base} -H.\033[0m")
