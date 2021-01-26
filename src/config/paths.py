import os
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent.parent
BOT_ENV_DIR = os.path.join(ROOT_DIR, "bot.env")
API_ENV_DIR = os.path.join(ROOT_DIR, "api.env")
