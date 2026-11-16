from datetime import datetime
from app.schemas import PlatformResult


class BasePlatform:
    name = "Base"
    public_access=self.is_public,
    async def post(self, message: str) -> str:
        raise NotImplementedError

    async def run(self, message: str) -> PlatformResult:
        try:
            url = await self.post(message)
            now = datetime.now()
            return PlatformResult(
                platform=self.name,
                status="success",
                posted_url=url,
                public_access=self.is_public,
                date=now.strftime("%Y-%m-%d"),
                time=now.strftime("%H:%M:%S"),
            )
        except Exception as e:
            return PlatformResult(
                platform=self.name,
                status="failed",
                error=str(e),
            )