from discord.ext import commands
from custom_errors import *


class GeneralErrorHandler(commands.Cog):
    """sends message on about on not able to execute a command"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        """catches exceptions and sends message relating to exception"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Sorry I did not catch that... type "?help" to see what I can do;) ')
        elif isinstance(error, NoMemberError):
            await ctx.send('Error 404 Guild Member Not Found...')
        elif isinstance(error, TooManySongs):
            await ctx.send("Sorry there are too many songs queued, can't get your song, try again later, sorry")
        elif isinstance(error, NoCityFound):
            await ctx.send("Can't find your specified city, double check your city name perhaps?")
