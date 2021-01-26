from functools import reduce
from operator import add
import os

from discord.ext import commands


def load_all_cogs(bot: commands.Bot) -> None:
    """Loads all the cogs for the bot. Assumes that the files that contain the cog contain the word cog and has a
    function called loader. It also assumes that the cog files are contained on directory deep in a folder that is in
    the same directory as this file """

    files_list = reduce(add, [f[2] for f in os.walk('.')])
    cog_files = filter(lambda x: 'cog' in x, files_list)
    cog_extensions = map(lambda x: x[:-3], cog_files)

    for cog in cog_extensions:
        bot.load_extension(cog)

