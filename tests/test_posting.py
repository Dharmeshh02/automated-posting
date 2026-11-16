from fastapi.testclient import TestClient
from app.main import app
from app.schemas import PostResponse, PlatformResult
from app.services import posting_service

client = TestClient(app)


def fake_result(name="Fake"):
    return PlatformResult(
        platform=name,
        status="success",
        posted_url="https://example.com/post/1",
        public_access=True,
        date="2026-11-16",
        time="10:00:00",
    )


def test_valid_message(monkeypatch):
    async def fake_post_to_all(message):
        return PostResponse(success=True, results=[fake_result()])

    monkeypatch.setattr("app.main.post_to_all", fake_post_to_all)
    r = client.post("/posting", json={"message": "Check this https://example.com"})
    assert r.status_code == 200
    assert r.json()["success"] is True


def test_no_link():
    r = client.post("/posting", json={"message": "Hello bina link ke"})
    assert r.status_code == 422


def test_two_links():
    r = client.post("/posting", json={"message": "https://a.com aur https://b.com"})
    assert r.status_code == 422


def test_too_long():
    msg = "a" * 200 + " https://example.com"
    r = client.post("/posting", json={"message": msg})
    assert r.status_code == 422


def test_invalid_url():
    r = client.post("/posting", json={"message": "Check https://nodot"})
    assert r.status_code == 422


def test_empty_message():
    r = client.post("/posting", json={"message": "   "})
    assert r.status_code == 422


def test_one_platform_fails_others_continue(monkeypatch):
    class Good:
        async def run(self, message):
            return fake_result("Good")

    class Bad:
        async def run(self, message):
            return PlatformResult(platform="Bad", status="failed", error="boom")

    monkeypatch.setattr(posting_service, "PLATFORMS", [Good(), Bad(), Good()])
    r = client.post("/posting", json={"message": "Check this https://example.com"})
    body = r.json()
    assert r.status_code == 200
    assert body["success"] is True
    assert [x["status"] for x in body["results"]] == ["success", "failed", "success"]