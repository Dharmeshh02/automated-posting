from fastapi import FastAPI
from app.schemas import PostRequest, PostResponse
from app.services.posting_service import post_to_all

app = FastAPI(title="Automated Multi-Platform Posting")


@app.post("/posting", response_model=PostResponse)
async def posting(data: PostRequest):
    return await post_to_all(data.message)