# Configuration file for environment variables (API keys, DB connection)
import dotenv
import os

dotenv.load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("BOT_TOKEN")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
