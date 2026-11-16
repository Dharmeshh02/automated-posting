import httpx
from datetime import datetime, timezone
from app.platforms.base import BasePlatform
from app import config

BASE = "https://bsky.social/xrpc"


class Bluesky(BasePlatform):
    name = "Bluesky"

    async def post(self, message: str) -> str:
        if not config.BLUESKY_HANDLE or not config.BLUESKY_APP_PASSWORD:
            raise Exception("Bluesky handle ya app password set nahi hai")

        handle = config.BLUESKY_HANDLE.strip().lstrip("@")

        async with httpx.AsyncClient(timeout=15) as client:
            # 1. Login
            s = await client.post(
                f"{BASE}/com.atproto.server.createSession",
                json={
                    "identifier": handle,
                    "password": config.BLUESKY_APP_PASSWORD.strip(),
                },
            )
            if s.status_code != 200:
                raise Exception(f"Bluesky login error {s.status_code}: {s.text[:150]}")
            session = s.json()

            # 2. Post
            r = await client.post(
                f"{BASE}/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {session['accessJwt']}"},
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": message,
                        "createdAt": datetime.now(timezone.utc).isoformat(),
                    },
                },
            )
            if r.status_code != 200:
                raise Exception(f"Bluesky post error {r.status_code}: {r.text[:150]}")

            rkey = r.json()["uri"].split("/")[-1]
            return f"https://bsky.app/profile/{handle}/post/{rkey}"