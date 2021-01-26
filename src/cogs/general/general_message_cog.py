import random

from discord.ext import commands
from discord import Embed, File

from common.resources import SPECIAL_IMG_PATH


class GeneralMessageCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.previous_member = None
        self.member_name = None

    @commands.command()
    async def about(self, ctx: commands.Context) -> None:
        """Sends a message on the who the bot is and the bot's maker"""
        cool_image_file = File(fp=SPECIAL_IMG_PATH, filename='special.jpg')

        # create and format embed
        about_embed = Embed(title="About",
                            description=f"Info on {self.bot.user.name}",
                            color=0xffa500)
        about_embed.add_field(name=f"Who I Am:",
                              value='I am A Spiritual Lyrical Miracle Individual',
                              inline=False)
        about_embed.add_field(name='Maker:', value="Made by Pectacius" + '\u1d48' + '\u1d49' + '\u1d5b')
        about_embed.set_image(url="attachment://special.jpg")
        await ctx.send(file=cool_image_file, embed=about_embed)

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        """Sends a message to greet the user, sends special message if member says hi more than once in a row"""
        author = ctx.author
        if self.previous_member is None or self.previous_member.id != author.id:
            await ctx.send(f'Greetings {author.name}')
            self.previous_member = author
        else:
            await ctx.send(f'Greeting {author.name}, this does seem familiar...')

    @commands.command()
    async def flip_coin(self, ctx: commands.Context, number: int) -> None:
        """Flips a coin <number> amount of times and sends result in chat"""
        for times in range(number):
            result = random.choice(['Heads', 'Tails'])
            await ctx.send(result)

    @commands.command()
    async def roll_dice(self, ctx: commands.Context, sides: int, number: int) -> None:
        """Rolls a <sides> sided die <number> amount of times and sends result in chat"""
        for times in range(number):
            result = random.choice(range(1, sides + 1))
            await ctx.send(f'{result}')


def setup(bot: commands.Bot) -> None:
    """Loads GeneralMessageCog"""
    bot.add_cog(GeneralMessageCog(bot))
