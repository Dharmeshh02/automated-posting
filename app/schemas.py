import re
from typing import Optional, List
from pydantic import BaseModel, field_validator

URL_PATTERN = re.compile(r"https?://\S+")
VALID_URL = re.compile(r"^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/\S*)?$")


class PostRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Message khali nahi ho sakta")

        if len(v) > 200:
            raise ValueError("Message 200 characters se zyada nahi ho sakta")

        links = URL_PATTERN.findall(v)
        if len(links) != 1:
            raise ValueError("Message mein exactly 1 link honi chahiye")

        if not VALID_URL.match(links[0]):
            raise ValueError("URL valid nahi hai")

        return v


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostResponse(BaseModel):
    success: bool
    results: List[PlatformResult]