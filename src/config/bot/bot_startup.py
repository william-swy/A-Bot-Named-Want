import os

from dotenv import load_dotenv

from config.config_paths import BOT_ENV_DIR

load_dotenv(BOT_ENV_DIR)

TOKEN = os.getenv('DISCORD_TOKEN')
ARRIVAL_CHANNEL = os.getenv('ARRIVAL_CHANNEL')
MUSIC_CHANNEL = os.getenv('MUSIC_CHANNEL')
WEATHER_CHANNEL = os.getenv('WEATHER_CHANNEL')

BOT_PREFIX = "!"
