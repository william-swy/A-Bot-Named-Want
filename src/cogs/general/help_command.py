import os
import random

from discord import Embed, File
from discord.ext.commands import HelpCommand, Command

from common.resources import HELP_IMG_PATH
from config.config import BOT_PREFIX


class Help(HelpCommand):
    """custom help command"""
    IMG_FILE = File(fp=HELP_IMG_PATH, filename='kermit.jpg')

    def __int__(self) -> None:
        """override the help description"""
        super().__init__(command_attrs={
            'help': 'Help description for bot, command, or a category'
        })

    async def send_bot_help(self, mapping) -> None:
        """sends an embed of docstring of all bot commands to invocation channel"""
        color = random.randint(0, 16777215)
        help_embed = Embed(title='Hippity Hoppity | Help',
                           description='For the ones that have forgotten or need a reminder...',
                           color=color)

        help_embed.add_field(name='Invocation Prefix:', value=f"Invoke commands with a `{BOT_PREFIX}`", inline=False)

        # remove key with value None
        mapping.pop(None)

        # add command docstrings to embed fields
        for key, value in mapping.items():
            if not value:
                continue

            for command in value:
                help_embed.add_field(name=f"`{command.name}`", value=command.help, inline=False)

        help_embed.add_field(name="Want more info about a specific command?",
                             value=f'Type `{BOT_PREFIX}<command_name>` for specific information!')
        help_embed.set_thumbnail(url="attachment://kermit.jpg")

        await super().get_destination().send(file=self.IMG_FILE, embed=help_embed)

    async def send_command_help(self, command: Command) -> None:
        """Sends an embed of details of <command>"""
        color = random.randint(0, 16777215)

        help_embed = Embed(title=f'Information for `{command.name}`', color=color)
        help_embed.add_field(name='Description', value=command.help, inline=False)
        help_embed.set_thumbnail(url='attachment://kermit.jpg')

        await super().get_destination().send(file=self.IMG_FILE, embed=help_embed)
