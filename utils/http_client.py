import httpx
from auth import auth
from utils.logger import get_logger

logger = get_logger("http_client") 

class HttpClient():
    def __init__(self, base_url: str):
        # 统一连接池 + 重试
        transport = httpx.AsyncHTTPTransport(retries=3)
        self.client = httpx.AsyncClient(
            base_url=base_url,
            transport=transport,
            timeout=30,
        )

    async def _request(self, method: str, path: str, user_id: str, **kw) -> httpx.Response:
        token = await auth.get_token(user_id)
        headers = kw.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        try:
            r = await self.client.request(method, path, headers=headers, **kw)
            trace_id = r.headers.get("trace-id") or "-"
            # 2. 响应后：记状态码+耗时（httpx 自带）
            logger.debug("[←] {} {}  status={}  trace-id={}",method.upper(), path, r.status_code, trace_id)
            r.raise_for_status()
            return r
        except httpx.HTTPStatusError as e:
            trace_id = e.response.headers.get("trace-id") or "-"
            logger.warning("[✗] {} {}  status={}  trace-id={}  response={}",
                method.upper(), path, e.response.status_code, trace_id, e.response.text
            )
            return f"{path} 响应异常，请稍后重试 (trace-id={trace_id})"

    async def close(self):
        await self.client.aclose()