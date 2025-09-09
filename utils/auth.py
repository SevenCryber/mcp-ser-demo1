import httpx
from cachetools import TTLCache
from auth.base import AuthBase
from settings import settings
from utils.logger import get_logger

logger = get_logger("auth") 

class Auth:
    _cache = TTLCache(maxsize=100, ttl=settings.hr_token_ttl - 60)
    
    async def get_token(self, user_id: str) -> str:
        if user_id in self._cache:
            return self._cache[user_id]
        logger.info("[user:%s] cache miss, requesting token", user_id)
        try:
            async with httpx.AsyncClient() as cli:
                r = await cli.post(
                    f"{settings.hr_base_url}/oauth/token",
                    data=dict(
                        grant_type="client_credentials",
                        client_id=settings.get_client_id(user_id),
                        client_secret=settings.get_client_secret(user_id),
                    ),
                )
                r.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error("[user:%s] http error %s - %s", user_id, e.response.status_code, e.response.text)
            raise
        except Exception:
            logger.exception("[user:%s] unexpected error while fetching token", user_id)
            raise
        token = r.json()["access_token"]
        self._cache[user_id] = token
        logger.info("[user:%s] token obtained and cached", user_id)
        return token