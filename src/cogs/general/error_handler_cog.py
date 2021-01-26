from discord.ext import commands

from common.Errors import botexceptions
from config.config import BOT_PREFIX


class ErrorHandlerCog(commands.Cog):
    """sends message on about on not able to execute a command"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        """catches exceptions and sends message relating to exception"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'Sorry I did not catch that... type "{BOT_PREFIX}help" to see what I can do;) ')
        elif isinstance(error, botexceptions.TooManySongs):
            await ctx.send("Sorry there are too many songs queued, can't get your song, try again later, sorry")


def setup(bot: commands.Bot) -> None:
    """Loads ErrorHandlerCog"""
    bot.add_cog(ErrorHandlerCog(bot))
