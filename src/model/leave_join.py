from discord.ext import commands
from discord.utils import get


# commands to let bot join and leave voice channels
class LeaveJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # bot will join your current voice channel. If bot is in another channel, it will join your current channel
    @commands.command()
    async def join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f'Joined {channel}')

    # bot will leave your current voice channel
    @commands.command()
    async def leave(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'Left {channel}')
