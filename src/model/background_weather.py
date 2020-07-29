import asyncio
import os
from datetime import datetime
from discord.ext import commands
import weather_query
from utils import CITY_DIR, TIMES_DIR


class BackgroundWeather:
    """schedules bot to send weather reports at specified times"""
    TIMES = None
    CURRENT_CITY = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.weather = weather_query.Weather()
        self.bot.loop.run_until_complete(self.initialize_settings())
        self.bot.loop.create_task(self.meteorology_report())

    async def meteorology_report(self) -> None:
        """sends a weather report at when current time matches designated time"""
        time_format = '%H:%M'
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.strftime(datetime.now(), time_format)
            if now in self.TIMES:
                channel = self.bot.get_channel(int(os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID')))
                await channel.send(f'This is your {self.TIMES[0]} weather report')

                # send reports for all cities
                for city in self.CURRENT_CITY:
                    weather_embed, weather_img = await self.weather.get_weather_report(city)
                    await channel.send(embed=weather_embed, file=weather_img)

                delay_time = 60
            else:
                delay_time = 1
            await asyncio.sleep(delay_time)

    async def initialize_settings(self) -> None:
        """reads and parses city.txt and times.txt to set designated cities and times"""
        with open(CITY_DIR, 'r') as city, open(TIMES_DIR) as times:
            self.CURRENT_CITY = city.read().split("/")
            self.TIMES = times.read().split(",")

            # remove delimiters
            del self.CURRENT_CITY[0]
            del self.TIMES[0]
