from mcp.server.fastmcp import FastMCP
import os
import httpx
import datetime



mcp = FastMCP("demo-server", host='0.0.0.0', port=8080)

@mcp.tool()
def print_current_time():
    print(f"Current time: {datetime.datetime.now()}")

@mcp.tool()
def fetch_data_from_api(url: str):
    response = httpx.get(url)
    return response.json()  

if __name__ == "__main__":
    mcp.run(transport='streamable-http')