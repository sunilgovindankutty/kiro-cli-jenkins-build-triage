import requests
from strands import tool


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city using wttr.in API."""
    resp = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    current = data["current_condition"][0]
    return (
        f"{city}: {current['temp_X']}°F, "
        f"{current['weatherDesc'][0]['value']}, "
        f"humidity {current['humidity']}%"
    )
