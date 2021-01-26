import asyncio
from decimal import Decimal
from typing import Tuple

import aiohttp
from discord import Embed, File

from common.Errors.botexceptions import NoCityFound, NoExistingWeatherData, NoWeatherDataInResponse
from common.resources import WEATHER_IMG_PATH
from config.config import WEATHER_KEY


class WeatherService:
    """
    make api request to openweathermap to get weather data
    """
    BASE_DAILY_WEATHER_URL = r'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}'
    BASE_WEATHER_EMOJI_URL = r'http://openweathermap.org/img/wn/{emoji}@2x.png'
    KELVIN_CELSIUS_DIFF = -273.15

    result = None
    data = {
        'Current temperature': '',
        'Feels like': '',
        'Current pressure': '',
        'Current humidity': '',
        'Weather description': '',
    }
    weather_location = None
    icon_url = None

    async def basic_search(self, city: str) -> None:
        """
        makes api request and returns temperature, feels like temp, pressure, humidity and description
        """
        complete_url = self.BASE_DAILY_WEATHER_URL.format(city_name=city, key=WEATHER_KEY)
        async with aiohttp.ClientSession() as session:
            async with session.get(complete_url) as response:
                self.result = await response.json()

    def parse_response(self) -> None:
        """
        Parses and transforms the request data for data to go into a weather report embed.
        """
        if self.data:
            if self.data['cod'] == '404':
                raise NoCityFound()
            else:
                specific_info = self.data['main']
                if specific_info:
                    # populate the dictionary named data with data from the response json
                    self.data['Current temperature'] = self.kelvin_to_celsius(specific_info['temp']) + u'\u2103'
                    self.data['Feels like'] = self.kelvin_to_celsius(specific_info['feels_like']) + u'\u2103'
                    self.data['Current pressure'] = str(specific_info['pressure']) + ' hPa'
                    self.data['Current humidity'] = str(specific_info['humidity']) + r' (percentage)'
                    self.data['Weather_description'] = self.data['weather'][0]['description']
                    self.weather_location = self.data['name'] + ', ' + self.data['sys']['country']
                    self.icon_url = self.BASE_WEATHER_EMOJI_URL.format(emoji=self.data['weather'][0]['icon'])
                else:
                    raise NoWeatherDataInResponse()
        else:
            raise NoExistingWeatherData()

    async def format_weather_report(self, city: str) -> Tuple[Embed, File]:
        """
        Creates a formatted weather report from the queried data
        :param city: The name of the city to generate a weather report for
        :return: A tuple with first element being the embed and the second element for the image in the embed
        """
        await self.basic_search(city)
        self.parse_response()

        for key, value in self.data.items():


        icon_url = self.grab_icon(icon)
        weather_descriptions = ['Current temperature', 'Feels like', 'Current pressure',
                                'Current humidity', 'Weather description']
        weather_pic = File(fp=WEATHER_IMG_PATH, filename='castform.jpg')
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


if __name__ == "__main__":
    async def test():
        weather = WeatherService()
        temp = await weather.basic_search("Truth or Consequences")
        print(temp)


    asyncio.run(test())
