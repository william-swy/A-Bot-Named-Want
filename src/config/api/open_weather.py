import os

from dotenv import load_dotenv

from config.paths import API_ENV_DIR

load_dotenv(API_ENV_DIR)

WEATHER_KEY = os.getenv('OPEN_WEATHER_MAP_KEY')