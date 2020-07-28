from discord.ext.commands import HelpCommand


class Help(HelpCommand):
    """custom help command"""
    def __int__(self):
        super.__init__()

    async def send_bot_help(self, mapping):
        #  todo stub

    async def send_cog_help(self, cog):
        # todo stub

    async def send_command_help(self, command):
        # todo stub

    async def get_command_signature(self, command):
        # todo stub

    async def send_group_help(self, group):
        # todo stub