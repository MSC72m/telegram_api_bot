# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_bot_token():
    """Retrieve the bot token from environment variables. the name of the variable is BOT_token by default"""
    return os.getenv("BOT_TOKEN")
