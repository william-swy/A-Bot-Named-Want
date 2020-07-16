import asyncio
import os
from datetime import datetime
from discord.ext import commands
import weather_query


# schedules bot to send weather reports at specified times
class BackgroundWeather:
    TIMES = ['09:00', '12:00', '21:00']
    CURRENT_CITY = 'calgary'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.weather = weather_query.Weather()
        self.bot.loop.create_task(self.meteorology_report())

    async def meteorology_report(self):
        time_format = '%H:%M'
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.strftime(datetime.now(), time_format)
            if now == self.TIMES[0]:
                embed = await self.weather.get_weather_report(self.CURRENT_CITY)
                channel = self.bot.get_channel(int(os.getenv('DISCORD_GENERAL_TALK_CHANNEL_ID')))
                await channel.send(f'This is your {self.TIMES[0]} weather report')
                await channel.send(embed=embed)
                first_time = self.TIMES[0]
                self.TIMES.pop(0)
                self.TIMES.append(first_time)
                delay_time = 90
            else:
                delay_time = 1
            await asyncio.sleep(delay_time)
