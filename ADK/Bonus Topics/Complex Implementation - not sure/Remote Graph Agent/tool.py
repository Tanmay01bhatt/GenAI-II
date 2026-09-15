from dotenv import load_dotenv
load_dotenv()
import os
import httpx
import asyncio

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_current_weather(city: str, units: str = "metric") -> dict:
    """Get current weather for a city.

    Args:
        city: City name, optionally "City,CountryCode" e.g. "Meerut,IN".
        units: "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin).

    Returns:
        dict with temperature, feels_like, humidity, description, wind_speed,
        or an "error" key if the request failed.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OPENWEATHER_API_KEY is not set."}

    params = {"q": city, "appid": api_key, "units": units}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"error": f"City '{city}' not found."}
        return {"error": f"Request failed: {e}"}
    except httpx.HTTPError as e:
        return {"error": f"Request failed: {e}"}

    return {
        "city": data["name"],
        "country": data["sys"].get("country"),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "units": units,
    }