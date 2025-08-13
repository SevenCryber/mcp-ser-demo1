# mcp-ser-demo1
my mcp server demo test

MCP Inspector调试
npx @modelcontextprotocol/inspector python weather_server.py

访问带token的url打开控制面板
STDIO模式
Command填写 python
Arguments填写 weather_server.py

SSE模式
python weather_server.py --transport sse --host 0.0.0.0 --port 8000
