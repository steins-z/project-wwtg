"""Data pipeline service: crawler + Redis cache (W1 stub)."""

from typing import Any


class DataService:
    """Manages POI data fetching and caching.
    
    W1: All methods return mock data.
    W2: Will integrate Playwright crawler + Redis cache + PostgreSQL persistence.
    """

    async def get_pois(self, city: str, tags: list[str]) -> list[dict[str, Any]]:
        """Fetch POIs for a city/tag combo from cache or crawler."""
        # W1 mock: return empty — plan_service uses hardcoded data
        return []

    async def refresh_cache(self, city: str) -> int:
        """Trigger a cache refresh for a city. Returns number of POIs updated."""
        # W1 stub
        return 0

    async def get_cache_stats(self) -> dict[str, Any]:
        """Return cache statistics."""
        return {"total_pois": 0, "cities_cached": [], "last_refresh": None}
