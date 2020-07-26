import aiohttp
import os
from discord.ext import commands
from discord import Embed
import custom_errors
from decimal import Decimal


class GetWeather(commands.Cog):
    """adds command to allow to get current weather of a city"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.weather_report = Weather()

    @commands.command()
    async def weather(self, ctx: commands.Context, city):
        """sends a weather report in chat of requested city"""
        embed = await self.weather_report.get_weather_report(city)
        await ctx.send(embed=embed)


class Weather:
    """make api request to openweathermap"""
    BASE_DAILY_WEATHER_URL = r'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}'
    BASE_WEATHER_EMOJI_URL = r'http://openweathermap.org/img/wn/{emoji}@2x.png'
    KELVIN_CELSIUS_DIFF = -273.15

    def __init__(self):
        self.WEATHER_KEY = os.getenv('WEATHER_TOKEN')

    async def basic_search(self, city):
        """makes api request and returns temperature, feels like temp, pressure, humidity and description"""
        complete_url = self.BASE_DAILY_WEATHER_URL.format(city_name=city, key=self.WEATHER_KEY)
        async with aiohttp.ClientSession() as session:
            async with session.get(complete_url) as response:
                data = await response.json()
                if data['cod'] != '404':
                    specific_info = data['main']
                    current_temperature = self.kelvin_to_celsius(specific_info['temp']) + u'\u2103'
                    feels_like = self.kelvin_to_celsius(specific_info['feels_like']) + u'\u2103'
                    current_pressure = str(specific_info['pressure']) + ' hPa'
                    current_humidity = str(specific_info['humidity']) + r' (percentage)'
                    weather_description = data['weather'][0]['description']
                    icon = data['weather'][0]['icon']
                    country = data['sys']['country']
                    city = data['name']
                    place = city + ', ' + country
                    return \
                        [current_temperature,
                         feels_like,
                         current_pressure,
                         current_humidity,
                         weather_description,
                         place], icon
                else:
                    raise custom_errors.NoCityFound()

    async def get_weather_report(self, city):
        """"create a embed with the weather data"""
        weather_data, icon = await self.basic_search(city)
        icon_url = self.grab_icon(icon)
        weather_descriptions = ['Current temperature', 'Feels like', 'Current pressure',
                                'Current humidity', 'Weather description']
        embed = Embed(title='Weather', description=f'Current weather in {weather_data[-1]}', color=0x0000ff)
        for description, data in zip(weather_descriptions, weather_data):
            embed.add_field(name=description, value=data, inline=False)
        embed.set_image(url=icon_url)
        return embed

    def grab_icon(self, icon):
        """returns url of png corresponding to the inputted icon encoding"""
        return self.BASE_WEATHER_EMOJI_URL.format(emoji=icon)

    def kelvin_to_celsius(self, temp):
        """converts a kelvin Decimal to a celsius string to 2 decimal places"""
        return str(round(Decimal(temp) + Decimal(self.KELVIN_CELSIUS_DIFF), 2))
