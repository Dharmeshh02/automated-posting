import httpx
from app.platforms.base import BasePlatform
from app import config


class Mastodon(BasePlatform):
    name = "Mastodon"

    async def post(self, message: str) -> str:
        if not config.MASTODON_TOKEN:
            raise Exception("MASTODON_TOKEN set nahi hai")

        base = (config.MASTODON_INSTANCE or "").strip().strip("\"'").rstrip("/")
        if not base.startswith("http"):
            base = "https://" + base.lstrip("/") if base else "https://mastodon.social"

        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                f"{base}/api/v1/statuses",
                headers={"Authorization": f"Bearer {config.MASTODON_TOKEN.strip()}"},
                data={"status": message, "visibility": "public"},
            )
            if r.status_code != 200:
                raise Exception(f"Mastodon error {r.status_code}: {r.text[:150]}")
            return r.json()["url"]