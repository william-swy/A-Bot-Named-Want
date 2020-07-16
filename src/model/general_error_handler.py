from discord.ext import commands
from custom_errors import *


# Handles errors thrown from commands
class GeneralErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Sorry I did not catch that... type "?help" to see what I can do;) ')
        elif isinstance(error, NoMemberError):
            await ctx.send('Error 404 Guild Member Not Found...')
        elif isinstance(error, TooManySongs):
            await ctx.send("Sorry there are too many songs queued, can't get your song, try again later, sorry")
        elif isinstance(error, NoCityFound):
            await ctx.send("Can't find your specified city, double check your city name perhaps?")
