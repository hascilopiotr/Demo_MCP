from mcp.server.fastmcp import FastMCP
import os
import httpx
import sys

print("[INFO] Starting MCP server...", file=sys.stderr)

# Load API key
api_key = os.getenv("OPENWEATHER_API_KEY", "")
print(f"[INFO] API key loaded: {bool(api_key)}", file=sys.stderr)

# Initialize MCP server
try:
    mcp = FastMCP("demo-server", host="0.0.0.0", port=8000)
    print("[INFO] FastMCP initialized", file=sys.stderr)
except Exception as e:
    print(f"[ERROR] Failed to initialize FastMCP: {e}", file=sys.stderr)
    sys.exit(1)

def get_api_key():
    """Helper to fetch latest API key from environment."""
    return os.getenv("OPENWEATHER_API_KEY", "")

@mcp.tool()
def check_api_key_status():
    """Check if the OpenWeather API key is loaded."""
    key = get_api_key()
    if key:
        masked = f"{key[:4]}{'*' * max(0, len(key) - 8)}{key[-4:]}"
        return {"status": "loaded", "api_key": masked, "length": len(key)}
    return {"status": "not_loaded", "error": "OPENWEATHER_API_KEY not set"}

@mcp.tool()
def get_weather(city: str, api_key_override: str = ""):
    """Fetches the current weather for a given city."""
    key_to_use = api_key_override or get_api_key()
    
    if not key_to_use:
        return {"error": "No API key provided or loaded"}
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key_to_use}&units=metric"
    
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data.get("name", city),
            "temperature": f"{data["main"]["temp"]}°C",
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        print("[INFO] Starting mcp.run() with streamable-http transport...", file=sys.stderr)
        mcp.run(transport="streamable-http")
    except Exception as e:
        print(f"[ERROR] Fatal error in mcp.run(): {e}", file=sys.stderr)
        sys.exit(1)
