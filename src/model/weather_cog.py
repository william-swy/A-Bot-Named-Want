from discord.ext import commands

import weather_query


class WeatherCog(commands.Cog):
    """adds command to allow to get current weather of a city"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializes bot and weather"""
        self.bot = bot
        self.weather_report = weather_query.Weather()

    @commands.command()
    async def weather(self, ctx: commands.Context, city: str) -> None:
        """Sends a weather report in chat of requested <city>"""
        weather_embed, image_file = await self.weather_report.get_weather_report(city)
        await ctx.send(embed=weather_embed, file=image_file)


def setup(bot: commands.Bot) -> None:
    """Loads WeatherCog"""
    bot.add_cog(WeatherCog(bot))
