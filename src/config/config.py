from config.bot import startup
from config.api import open_weather

# Bot related environment variable values
TOKEN = startup.TOKEN
BOT_PREFIX = startup.BOT_PREFIX
ARRIVAL_CHANNEL = startup.ARRIVAL_CHANNEL
MUSIC_CHANNEL = startup.MUSIC_CHANNEL
WEATHER_CHANNEL = startup.WEATHER_CHANNEL

# API related environment variable values
WEATHER_KEY = open_weather.WEATHER_KEY
