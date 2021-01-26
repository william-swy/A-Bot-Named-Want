import os
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent.parent
RESOURCE_DIR = os.path.join(ROOT_DIR, "resources")

WELCOME_GIF_PATH = os.path.join(RESOURCE_DIR, "welcome.gif")
HELP_IMG_PATH = os.path.join(RESOURCE_DIR, "kermit.jpg")
SPECIAL_IMG_PATH = os.path.join(RESOURCE_DIR, "peepo.jpg")

WEATHER_IMG_PATH = os.path.join(RESOURCE_DIR, "weather.png")
WEATHER_SETTINGS_PATH = os.path.join(RESOURCE_DIR, "weather_config.json")

MUSIC_IMG_PATH = os.path.join(RESOURCE_DIR, "music.jpg")
MUSIC_FILES_DIR = os.path.join(RESOURCE_DIR, "cached_music")