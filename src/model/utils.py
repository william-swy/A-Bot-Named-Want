from pathlib import Path
import os

# PATHS of various files
ROOT_DIR = Path(__file__).parent.parent.parent

DATA_DIR = os.path.join(ROOT_DIR, 'data')
SRC_DIR = os.path.join(ROOT_DIR, 'src')
MAIN_DIR = os.path.join(SRC_DIR, 'model')

WELCOME_IMG_PATH = os.path.join(DATA_DIR, 'welcome.gif')
WEIRD_PATH = os.path.join(DATA_DIR, 'oof.jpg')
ROBLOX_PATH = os.path.join(DATA_DIR, 'roblox.jpg')
YES_PATH = os.path.join(DATA_DIR, 'yes.jpg')
ENV_PATH = os.path.join(DATA_DIR, '.env')
PREFIX_DIR = os.path.join(DATA_DIR, 'prefix.txt')

WEATHER_DIR = os.path.join(DATA_DIR, 'weather')
CITY_DIR = os.path.join(WEATHER_DIR, 'city.txt')
TIMES_DIR = os.path.join(WEATHER_DIR, 'times.txt')
