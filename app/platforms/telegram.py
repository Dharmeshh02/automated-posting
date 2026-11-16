import httpx
from app.platforms.base import BasePlatform
from app import config


class Telegram(BasePlatform):
    name = "Telegram"

    async def post(self, message: str) -> str:
        if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
            raise Exception("Telegram token ya chat id set nahi hai")

        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                url,
                json={"chat_id": config.TELEGRAM_CHAT_ID, "text": message},
            )
            data = r.json()
            if not data.get("ok"):
                raise Exception(f"Telegram error: {data.get('description')}")
            result = data["result"]
            username = result["chat"].get("username")
            if not username:
                raise Exception("Channel public nahi hai, link nahi ban sakta")
            return f"https://t.me/{username}/{result['message_id']}"