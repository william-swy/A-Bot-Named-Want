from pathlib import Path
import os

# PATHS of various files
ROOT_DIR = Path(__file__).parent.parent.parent

DATA_DIR = os.path.join(ROOT_DIR, 'data')
ENV_PATH = os.path.join(DATA_DIR, '.env')
PREFIX_DIR = os.path.join(DATA_DIR, 'prefix.txt')

SRC_DIR = os.path.join(ROOT_DIR, 'src')

MAIN_DIR = os.path.join(SRC_DIR, 'model')

IMAGE_DIR = os.path.join(DATA_DIR, 'images')
WELCOME_IMG_PATH = os.path.join(IMAGE_DIR, 'welcome.gif')

WEATHER_DIR = os.path.join(DATA_DIR, 'weather')
CITY_DIR = os.path.join(WEATHER_DIR, 'city.txt')
TIMES_DIR = os.path.join(WEATHER_DIR, 'times.txt')

# constants
with open(PREFIX_DIR, 'r') as file:
    PREFIX = file.read()
    file.close()
