from discord.ext import commands
from discord.utils import get


class LeaveJoin(commands.Cog):
    """commands to let bot join and leave voice channels"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def join(self, ctx: commands.Context) -> None:
        """bot will join your current voice channel. If bot is in another channel, it will join your current channel"""
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f'Joined {channel}')

    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        """bot will leave your current voice channel"""
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'Left {channel}')
