from abc import ABC, abstractmethod
from typing import Optional

class AuthBase(ABC):
    @abstractmethod
    async def get_token(self, user_id: str) -> str:
        """返回可用 token，内部做缓存/续期"""