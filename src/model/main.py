import os

import background_weather
import bot_leave_join
import general_error_handler
import general_message
import member_manager
import music
import utils
import weather_query
from discord.ext import commands
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(utils.ENV_PATH)

    BOT_COMMAND_PREFIX = '<@&724830609238917192>'
    TOKEN = os.getenv('DISCORD_TOKEN')
    GENERAL_CHANNEL_ID = os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID')
    PREFIX_DIR = utils.DATA_DIR + '\\prefix.txt'

    # get prefix from file
    with open(PREFIX_DIR, 'r') as file:
        prefix = file.read()
        file.close()

    # initialize bot
    bot = commands.Bot(command_prefix=prefix, description='A multipurpose bot')
    bot.remove_command("help")

    # add cogs
    bot.add_cog(member_manager.MemberManager(bot))
    bot.add_cog(general_message.GeneralMessage(bot))
    bot.add_cog(general_error_handler.GeneralErrorHandler(bot))
    bot.add_cog(bot_leave_join.LeaveJoin(bot))
    bot.add_cog(music.Music(bot))
    bot.add_cog(weather_query.GetWeather(bot))

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
    bot.loop.run_until_complete(weather_man.initialize_settings())
    bot.loop.create_task(weather_man.meteorology_report())

    # run bot
    bot.run(TOKEN)
