from discord.ext import commands


class WeatherCog(commands.Cog):
    """adds command to allow to get current weather of a city"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializes bot and weather"""
        self.bot = bot
        self.weather_report = Weather()

    @commands.command()
    async def weather(self, ctx: commands.Context, city: str) -> None:
        """Sends a weather report in chat of requested <city>"""
        weather_embed, image_file = await self.weather_report.get_weather_report(city)
        await ctx.send(embed=weather_embed, file=image_file)