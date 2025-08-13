#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一个示范 MCP Server：
  - 提供 1 个 Tool：get_weather
  - 提供 1 个 Resource：weather://cities
  - 提供 1 个 Prompt：travel_guide
同时支持 stdio 与 SSE 两种传输方式，启动时通过命令行参数切换。
"""
import json
import asyncio
import argparse
from typing import Any
from mcp.server.fastmcp import FastMCP

# 1. 创建 MCP 实例
mcp = FastMCP("weather-demo")

# 2. 工具：天气查询（mock）
@mcp.tool()
async def get_weather(city: str) -> str:
    """查询城市天气（仅示例）"""
    fake_db = {
        "beijing":  "晴，25℃",
        "shanghai": "多云，22℃",
        "guangzhou":"小雨，20℃"
    }
    return fake_db.get(city.lower(), "未收录该城市")

# 3. 资源：城市列表
@mcp.resource("weather://cities")
def list_cities() -> str:
    return json.dumps(["beijing", "shanghai", "guangzhou"])

# 4. 提示模板：旅行指南
@mcp.prompt()
def travel_guide(city: str) -> str:
    return f"""
请扮演资深旅行顾问，为一位首次前往 {city} 的游客提供：
1. 三天两晚行程建议
2. 必吃美食
3. 交通与住宿 Tips
"""

# 5. 命令行双协议启动
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")