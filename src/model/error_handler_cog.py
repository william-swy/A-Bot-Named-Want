from discord.ext import commands

import custom_errors
import utils


class ErrorHandlerCog(commands.Cog):
    """sends message on about on not able to execute a command"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        """catches exceptions and sends message relating to exception"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'Sorry I did not catch that... type "{utils.PREFIX}help" to see what I can do;) ')
        elif isinstance(error, custom_errors.NoMemberError):
            await ctx.send('Error 404 Guild Member Not Found...')
        elif isinstance(error, custom_errors.TooManySongs):
            await ctx.send("Sorry there are too many songs queued, can't get your song, try again later, sorry")
        elif isinstance(error, custom_errors.NoCityFound):
            await ctx.send("Can't find your specified city, double check your city name perhaps?")


def setup(bot: commands.Bot) -> None:
    """Loads ErrorHandlerCog"""
    bot.add_cog(ErrorHandlerCog(bot))
