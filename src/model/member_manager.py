import os
import utils
from discord import File
from discord.ext import commands


# handles member join and leave
class MemberManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # sends general to guild and private to member when new member joins,
    # will send special image if member is new to guild
    @commands.Cog.listener()
    async def on_member_join(self, member):
        general_channel_id = int(os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID'))
        general_channel = self.bot.get_channel(general_channel_id)

        await member.create_dm()

        if member.joined_at is None:
            await member.dm_channel.send(
                f"""Hi {member.name}, welcome to {os.getenv('DISCORD_SERVER_NAME')}!\n 
                I hAvE bEEn WAiTinG fOR yOU...( ͡° ͜ʖ ͡°) HEHE"""
            )
            await general_channel.send(f"LET'S WELCOME {member.name} RAH! RAH! \U0001F389")
            await general_channel.send(file=File(utils.WELCOME_IMG_PATH))
        else:
            await member.dm_channel.send("Welcome Back! YAY! YAY!")
            await general_channel.send(f'{member.name} IS BACK.. WITH SOME SNACKS!')
