from discord.ext import commands

from cogs.general import help_command
from cogs.loader import load_all_cogs
from config import config

bot = commands.Bot(command_prefix=config.BOT_PREFIX, help_command=help_command.Help())

load_all_cogs(bot)


@bot.event
async def on_ready():
    print("hi")


bot.run(config.TOKEN)
