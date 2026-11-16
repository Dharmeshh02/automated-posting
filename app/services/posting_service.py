import asyncio
from app.platforms.discord import Discord
from app.platforms.telegram import Telegram
from app.platforms.mastodon import Mastodon
from app.platforms.bluesky import Bluesky
from app.platforms.devto import DevTo
from app.schemas import PostResponse
PLATFORMS = [Discord(), Telegram(), Mastodon(), Bluesky(), DevTo()]
async def post_to_all(message: str) -> PostResponse:
    results = await asyncio.gather(*(p.run(message) for p in PLATFORMS))
    success = any(r.status == "success" for r in results)
    return PostResponse(success=success, results=list(results))