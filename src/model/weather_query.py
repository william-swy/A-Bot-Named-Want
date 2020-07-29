from decimal import Decimal
import os
from typing import Tuple, List

import aiohttp
from discord import Embed, File

import custom_errors
import utils


class Weather:
    """make api request to openweathermap"""
    BASE_DAILY_WEATHER_URL = r'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}'
    BASE_WEATHER_EMOJI_URL = r'http://openweathermap.org/img/wn/{emoji}@2x.png'
    KELVIN_CELSIUS_DIFF = -273.15
    CASTFORM_DIR = os.path.join(utils.IMAGE_DIR, 'castform.jpg')

    def __init__(self) -> None:
        self.WEATHER_KEY = os.getenv('WEATHER_TOKEN')

    async def basic_search(self, city: str) -> Tuple[List, str]:
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

    async def get_weather_report(self, city: str) -> Tuple[Embed, File]:
        """"create a embed with the weather data"""
        weather_data, icon = await self.basic_search(city)
        icon_url = self.grab_icon(icon)
        weather_descriptions = ['Current temperature', 'Feels like', 'Current pressure',
                                'Current humidity', 'Weather description']
        weather_pic = File(fp=self.CASTFORM_DIR, filename='castform.jpg')
        weather_embed = Embed(title='Weather', description=f'Current weather in {weather_data[-1]}', color=0x0000ff)
        for description, data in zip(weather_descriptions, weather_data):
            weather_embed.add_field(name=description, value=data, inline=False)
        weather_embed.set_image(url=icon_url)
        weather_embed.set_thumbnail(url='attachment://castform.jpg')
        return weather_embed, weather_pic

    def grab_icon(self, icon: str) -> str:
        """returns url of png corresponding to the inputted icon encoding"""
        return self.BASE_WEATHER_EMOJI_URL.format(emoji=icon)

    def kelvin_to_celsius(self, temp: str) -> str:
        """converts a kelvin Decimal to a celsius string to 2 decimal places"""
        return str(round(Decimal(temp) + Decimal(self.KELVIN_CELSIUS_DIFF), 2))
