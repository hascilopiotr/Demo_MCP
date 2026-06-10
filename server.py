from mcp.server.fastmcp import FastMCP
import os
import httpx
import requests

mcp = FastMCP("demo-server", host="0.0.0.0", port=8000)

def get_api_key():
    """Helper to ensure we always fetch the latest env variable."""
    return os.getenv("OPENWEATHER_API_KEY")

@mcp.tool()
def check_api_key_status():
    """Check if the OpenWeather API key is loaded."""
    key = get_api_key()
    if key:
        masked = f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"
        return {"status": "loaded", "api_key": masked}
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
    mcp.run(transport="streamable-http")

