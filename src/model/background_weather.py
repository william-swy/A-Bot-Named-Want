import asyncio
import os
from datetime import datetime
from discord.ext import commands
import weather_query
from utils import CITY_DIR, TIMES_DIR


# schedules bot to send weather reports at specified times
class BackgroundWeather:
    TIMES = None
    CURRENT_CITY = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.weather = weather_query.Weather()

    async def meteorology_report(self):
        time_format = '%H:%M'
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.strftime(datetime.now(), time_format)
            if now == self.TIMES[0]:
                channel = self.bot.get_channel(int(os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID')))
                await channel.send(f'This is your {self.TIMES[0]} weather report')

                # send reports for all cities
                for city in self.CURRENT_CITY:
                    embed = await self.weather.get_weather_report(city)
                    await channel.send(embed=embed)

                first_time = self.TIMES[0]
                self.TIMES.pop(0)
                self.TIMES.append(first_time)
                delay_time = 90
            else:
                delay_time = 1
            await asyncio.sleep(delay_time)

    # get cities and times
    async def initialize_settings(self):
        with open(CITY_DIR, 'r') as city, open(TIMES_DIR) as times:
            self.CURRENT_CITY = city.read().split("/")
            self.TIMES = times.read().split(",")

            # remove delimiters
            del self.CURRENT_CITY[0]
            del self.TIMES[0]
