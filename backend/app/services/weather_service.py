"""Weather API client (W1 mock)."""

from typing import Any


class WeatherService:
    """Fetches weather forecasts for plan generation.
    
    W1: Returns hardcoded weather data.
    W2: Will integrate wttr.in or 和风天气 API.
    """

    async def get_forecast(self, city: str, days: int = 2) -> dict[str, Any]:
        """Get weather forecast for upcoming days."""
        return {
            "city": city,
            "forecasts": [
                {
                    "date": "明天",
                    "temp_low": 7,
                    "temp_high": 15,
                    "condition": "多云",
                    "suggestion": "建议穿薄外套",
                },
                {
                    "date": "后天",
                    "temp_low": 10,
                    "temp_high": 18,
                    "condition": "晴",
                    "suggestion": "适合户外活动",
                },
            ],
        }
