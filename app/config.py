import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MASTODON_INSTANCE = os.getenv("MASTODON_INSTANCE") or "https://mastodon.social"
MASTODON_TOKEN = os.getenv("MASTODON_TOKEN")
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")