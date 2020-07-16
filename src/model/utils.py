from pathlib import Path
import os

# PATHS of various files
ROOT_DIR = Path(__file__).parent.parent.parent

DATA_DIR = os.path.join(ROOT_DIR, 'data')
MAIN_DIR = os.path.join(ROOT_DIR, 'src\\model')

WELCOME_IMG_PATH = os.path.join(ROOT_DIR, 'data\\welcome.gif')
WEIRD_PATH = os.path.join(ROOT_DIR, 'data\\oof.jpg')
ROBLOX_PATH = os.path.join(ROOT_DIR, 'data\\roblox.jpg')
YES_PATH = os.path.join(ROOT_DIR, 'data\\yes.jpg')
ENV_PATH = os.path.join(ROOT_DIR, 'data\\.env')
