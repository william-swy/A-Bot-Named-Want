from discord.ext import commands

from cogs.weather import weatherservice
from common.Errors.botexceptions import NoCityFound


class WeatherCog(commands.Cog):
    """adds command to allow to get current weather of a city"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializes bot and weather"""
        self.bot = bot
        self.weather_report = weatherservice.WeatherService()

    @commands.command()
    async def weather(self, ctx: commands.Context, city: str) -> None:
        """Sends a weather report in chat of requested <city>"""
        try:
            weather_embed, image_file = await self.weather_report.get_weather_report(city)
            await ctx.send(embed=weather_embed, file=image_file)
        except NoCityFound as error:
            await ctx.send(f"Can't find {city}, double check your city name perhaps?")


def setup(bot: commands.Bot) -> None:
    """Loads WeatherCog"""
    bot.add_cog(WeatherCog(bot))
