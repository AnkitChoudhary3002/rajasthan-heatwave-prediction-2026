import requests

OPENWEATHER_API_KEY = "a4ba406145a3cc34128bccc6f8cab9a6"  # Get free key from openweathermap.org
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city_name: str) -> dict:
    """Fetch real-time weather data for a city."""
    params = {
            "q": city_name,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Celsius
        }

    response = requests.get(OPENWEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "windspeed": round((data["wind"]["speed"] * 3.6), 3),  # m/s to km/h
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"]
            }
    else:
        raise Exception(f"City not found or API error: {response.status_code}")