import asyncio
from datetime import datetime
import json

from discord.ext import commands

from cogs.weather import weatherservice
from config.config import WEATHER_CHANNEL
from common.Errors.botexceptions import NoCityFound
from common.resources import WEATHER_SETTINGS_PATH


class BackgroundWeather:
    """schedules bot to send weather reports at specified times"""
    TIMES = None
    CURRENT_CITY = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.weather = weatherservice.WeatherService()
        self.bot.loop.run_until_complete(self.initialize_settings())
        self.bot.loop.create_task(self.meteorology_report())

    async def meteorology_report(self) -> None:
        """sends a weather report at when current time matches designated time"""
        time_format = '%H:%M'
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.strftime(datetime.utcnow(), time_format)
            if now in self.TIMES:
                channel = self.bot.get_channel(int(WEATHER_CHANNEL))
                await channel.send(f'This is your {now} UTC weather report')

                # send reports for all cities
                for city in self.CURRENT_CITY:
                    try:
                        weather_embed, weather_img = await self.weather.get_weather_report(city)
                        await channel.send(embed=weather_embed, file=weather_img)
                    except NoCityFound as error:
                        pass

                delay_time = 60
            else:
                delay_time = 1
            await asyncio.sleep(delay_time)

    async def initialize_settings(self) -> None:
        """reads and parses city.txt and times.txt to set designated cities and times"""
        with open(WEATHER_SETTINGS_PATH, 'r') as settings:
            data = json.load(settings)
            self.CURRENT_CITY = data["cities"]
            self.TIMES = data["times"]
