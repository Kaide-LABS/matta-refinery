import httpx

class DriveClient:
    def __init__(self, base_url: str = "http://localhost:8092/drive"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def create_doc(self, title: str) -> dict:
        resp = await self.client.post(f"{self.base_url}/files", json={"title": title})
        resp.raise_for_status()
        return resp.json()

    async def update_doc(self, file_id: str, content: str) -> dict:
        resp = await self.client.patch(f"{self.base_url}/files/{file_id}", json={"content": content})
        resp.raise_for_status()
        return resp.json()

    async def generate_share_link(self, file_id: str) -> str:
        resp = await self.client.post(f"{self.base_url}/files/{file_id}/permissions")
        resp.raise_for_status()
        return resp.json().get("web_view_link", "")
