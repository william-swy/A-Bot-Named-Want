from discord.ext import commands

from cogs.general import help_command
from config import config

bot = commands.Bot(command_prefix=config.BOT_PREFIX, help_command=help_command.Help())


@bot.event
async def on_ready():
    print("hi")


bot.run(config.TOKEN)
