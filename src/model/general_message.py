from discord.ext import commands
from custom_errors import NoMemberError
from discord import Embed, File
import random
import utils


class GeneralMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.previous_member = None
        self.member_name = None

    @commands.command()
    async def who(self, ctx: commands.Context, *, args):
        lower_args = args.lower()
        if lower_args.find("are you") == 0:
            await ctx.send("a sPIRITUAL lYRICAL mIRACLE iNDIVIDUAL")
            await ctx.send(file=File(utils.YES_PATH))
        elif lower_args.find("made you") == 0:
            await ctx.send("Made by the magnificent Pectacius")
        else:
            await ctx.send("Sorry didn't understand that")

        """if len(args) == 2:
            if args[1] == "you?" or args[1] == "you":
                if args[0] == "are":
                    await ctx.send("a sPIRITUAL lYRICAL mIRACLE iNDIVIDUAL")
                    await ctx.send(file=File(utils.YES_PATH))
                elif args[0] == "made":
                    await ctx.send("Made by the magnificent Pectacius")
                else:
                    raise commands.CommandNotFound
            else:
                raise commands.CommandNotFound
        else:
            raise commands.CommandNotFound"""

    @commands.command()
    async def hi(self, ctx: commands.Context):
        author = ctx.author
        if self.previous_member is None or self.previous_member.id != author.id:
            await ctx.send(f'Greetings {author.name}')
            self.previous_member = author
        else:
            await ctx.send(f'Greeting {author.name}, this does seem familiar...')

    @commands.command(name='help')
    async def help_me(self, ctx: commands.Context):
        command_dict = {
            'who are you?': 'info on BOT_Pectacius',
            'who made you?': 'maker of BOT_Pectacius',
            'hi': "the bot is lonely, say hi;)",
            'roast <@member_name>': 'roasts <member_name> with a cheesy roast (accepts "me" as arg)',
            'join': 'makes bot join your current voice channel',
            'leave': 'makes bot leave your current voice channel',
            'play <song name>': 'plays song in music voice channel, will queue song if another song is playing',
            'skip': 'plays next song in music queue',
            'pause': 'pauses current song',
            'queue <song name>': 'adds song to queue',
            'resume': 'resumes playing paused song',
            'weather <city name>': 'displays current weather in <city name>',
            'flip_coin <num_of_coins>': 'flips a given number of coin(s) one time',
            'roll_dice <num_of_sides> <num_of_dice>': 'rolls given number of dice a given number of times'
        }
        msg = Embed(title='BOT_Pectacius Commands',
                    description='List of what BOT_Pectacius can do for you.\n Type "?" followed by command:)',
                    color=0x0000ff)
        for ability, description in command_dict.items():
            msg.add_field(name=ability, value=description, inline=False)
        await ctx.send(embed=msg)

    @commands.command()
    async def roast(self, ctx: commands.Context, member):
        guild_members = self.bot.get_all_members()
        member_obj = await commands.MemberConverter().convert(ctx, member)

        roasts = {'roblox': ['stop being having autism', "go commit breathn't", 'you were born out of your dad',
                             'you think you funny but look at ya hairline be looking like the macdondald symble',
                             'do you are have stupid', 'yeetus yeetus commit self deletus'],
                  'weirdness': ['ur a trophy{}\n a catas..trophy'.format('\n...' * 3),
                                'ur pretty{}\n pretty ugly'.format('\n...' * 3)]}

        roast = random.choice(list(roasts.items()))
        the_roast = random.choice(roast[1])

        if member_obj in guild_members:
            self.member_name = member_obj.name

            await ctx.send(f'{self.member_name}\n{the_roast}')

            if roast[0] == 'roblox':
                await ctx.send(file=File(utils.ROBLOX_PATH))
            if roast[0] == 'weirdness':
                await ctx.send(file=File(utils.WEIRD_PATH))
        else:
            raise NoMemberError

    @commands.command()
    async def flip_coin(self, ctx: commands.Context, number: int):
        for times in range(number):
            result = random.choice(['Heads', 'Tails'])
            await ctx.send(result)

    @commands.command()
    async def roll_dice(self, ctx: commands.Context, sides: int, number: int):
        for times in range(number):
            result = random.choice(range(1, sides + 1))
            await ctx.send(f'{result}')
