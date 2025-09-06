import httpx
from cachetools import TTLCache
from auth.base import AuthBase
from settings import settings

class HRAuth(AuthBase):
    _cache = TTLCache(maxsize=100, ttl=settings.hr_token_ttl - 60)  # 提前 60s 续期

    async def get_token(self, user_id: str) -> str:
        if user_id not in self._cache:          # 按用户隔离
            async with httpx.AsyncClient() as cli:
                r = await cli.post(
                    f"{settings.hr_base_url}/oauth/token",
                    data=dict(
                        grant_type="client_credentials",
                        client_id=settings.get_client_id(user_id),   # 各用户自己的密钥
                        client_secret=settings.get_client_secret(user_id),
                    ),
                )
                r.raise_for_status()
                self._cache[user_id] = r.json()["access_token"]
        return self._cache[user_id]