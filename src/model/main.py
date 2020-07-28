import os

import background_weather
import leave_join
import general_error_handler
import general_message
import member_manager
import music
import utils
import weather_query
from help_command import Help
from discord.ext import commands
from dotenv import load_dotenv

if __name__ == "__main__":
    # load keys in environment variables
    load_dotenv(utils.ENV_PATH)

    TOKEN = os.getenv('DISCORD_TOKEN')
    GENERAL_CHANNEL_ID = os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID')

    # initialize bot
    bot = commands.Bot(command_prefix=utils.PREFIX, description='A multipurpose bot', help_command=Help())
    bot.remove_command("help")

    # add cogs
    bot.add_cog(member_manager.MemberManager(bot))
    bot.add_cog(general_message.GeneralMessage(bot))
    bot.add_cog(general_error_handler.GeneralErrorHandler(bot))
    bot.add_cog(leave_join.LeaveJoin(bot))
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
