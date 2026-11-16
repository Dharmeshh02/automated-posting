import httpx
from app.platforms.base import BasePlatform
from app import config


class Discord(BasePlatform):
    name = "Discord"
   is_public = False
    async def post(self, message: str) -> str:
        if not config.DISCORD_WEBHOOK_URL:
            raise Exception("DISCORD_WEBHOOK_URL set nahi hai")

        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                config.DISCORD_WEBHOOK_URL + "?wait=true",
                json={"content": message},
            )
            r.raise_for_status()
            data = r.json()
            return f"https://discord.com/channels/{data.get('guild_id', '@me')}/{data['channel_id']}/{data['id']}"