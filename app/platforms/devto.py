import httpx
from app.platforms.base import BasePlatform
from app import config


class DevTo(BasePlatform):
    name = "Dev.to"

    async def post(self, message: str) -> str:
        if not config.DEVTO_API_KEY:
            raise Exception("DEVTO_API_KEY set nahi hai")

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(
                "https://dev.to/api/articles",
                headers={
                    "api-key": config.DEVTO_API_KEY.strip(),
                    "Accept": "application/vnd.forem.api-v1+json",
                },
                json={
                    "article": {
                        "title": "Update: " + message.split("http")[0].strip()[:50],
                        "body_markdown": message,
                        "published": True,
                    }
                },
            )
            if r.status_code not in (200, 201):
                raise Exception(f"Dev.to error {r.status_code}: {r.text[:150]}")
            return r.json()["url"]