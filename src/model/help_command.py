from discord.ext.commands import HelpCommand


class Help(HelpCommand):
    """custom help command"""

    def __int__(self) -> None:
        """override the help description"""
        super().__init__(command_attrs={
            'help': 'Help description for bot, command, or a category'
        })

    async def send_bot_help(self, mapping):
        pass  # todo stub

    async def send_cog_help(self, cog):
        pass  # todo stub

    async def send_command_help(self, command):
        pass  # todo stub

    async def get_command_signature(self, command):
        pass  # todo stub

    async def send_group_help(self, group):
        pass  # todo stub
