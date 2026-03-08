import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://YOUR_GITHUB_USERNAME.github.io/ubt-mini-app/")
