import httpx
from abc import ABC
from auth.base import AuthBase

class BaseClient(ABC):
    def __init__(self, auth: AuthBase, base_url: str):
        self.auth = auth
        self.base_url = base_url
        # 统一连接池 + 重试
        transport = httpx.AsyncHTTPTransport(retries=3)
        self.client = httpx.AsyncClient(
            base_url=base_url,
            transport=transport,
            timeout=30,
        )

    async def _request(self, method: str, path: str, user_id: str, **kw) -> httpx.Response:
        token = await self.auth.get_token(user_id)
        headers = kw.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        r = await self.client.request(method, path, headers=headers, **kw)
        r.raise_for_status()
        return r

    async def close(self):
        await self.client.aclose()