import httpx

class SlackClient:
    def __init__(self, token: str, base_url: str = "http://localhost:8090/api"):
        self.token = token
        self.base_url = base_url
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {self.token}"})

    async def post_message(self, channel: str, blocks: list) -> dict:
        resp = await self.client.post(f"{self.base_url}/chat.postMessage", json={
            "channel": channel,
            "blocks": blocks
        })
        resp.raise_for_status()
        return resp.json()

    async def update_canvas(self, canvas_id: str, blocks: list) -> dict:
        resp = await self.client.post(f"{self.base_url}/canvases.edit", json={
            "canvas_id": canvas_id,
            "blocks": blocks
        })
        resp.raise_for_status()
        return resp.json()
