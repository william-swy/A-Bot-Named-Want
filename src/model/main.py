import os

from discord.ext import commands
from dotenv import load_dotenv
from src.cogs.general.help_command import Help

from src.cogs.weather import background_weather
import utils

if __name__ == "__main__":
    # load keys in environment variables
    load_dotenv(utils.ENV_PATH)

    TOKEN = os.getenv('DISCORD_TOKEN')
    GENERAL_CHANNEL_ID = os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID')

    # initialize bot
    bot = commands.Bot(command_prefix=utils.PREFIX, description='A multipurpose bot', help_command=Help())

    # add cogs
    cog_files_list = [f for f in os.listdir(utils.MAIN_DIR) if 'cog' in f]
    cog_extensions = map(lambda x: x[:-3], cog_files_list)
    for cog in cog_extensions:
        bot.load_extension(cog)

    # connection confirmation
    @bot.event
    async def on_ready():
        servers = bot.guilds
        server_names = '\n - '.join(f'{guild.name} (id: {guild.id})' for guild in servers)
        print(f'{bot.user.name} has connected to %d server(s):\n - %s' % (len(servers), server_names))

        online_msg = f'{bot.user.name} is ready to roll!'
        channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
        await channel.send(online_msg)

    # initialize the scheduled weather reports
    weather_man = background_weather.BackgroundWeather(bot)

    # run bot
    bot.run(TOKEN)
