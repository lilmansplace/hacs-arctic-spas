"""API client for Arctic Spa."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

from .const import API_BASE_URL, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class ArcticSpaApiError(Exception):
    """Base exception for Arctic Spa API errors."""


class ArcticSpaAuthError(ArcticSpaApiError):
    """Authentication error."""


class ArcticSpaConnectionError(ArcticSpaApiError):
    """Connection error."""


class ArcticSpaApiClient:
    """Client for the Arctic Spa cloud API."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self._api_key = api_key
        self._session = session
        self._headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Make an API request."""
        url = f"{API_BASE_URL}{endpoint}"
        try:
            async with asyncio.timeout(API_TIMEOUT):
                async with self._session.request(
                    method, url, headers=self._headers, json=json_data
                ) as resp:
                    if resp.status == 401:
                        raise ArcticSpaAuthError("Invalid API key")
                    if resp.status == 403:
                        raise ArcticSpaAuthError("API key not authorized")
                    resp.raise_for_status()
                    if resp.content_type == "application/json":
                        return await resp.json()
                    return None
        except asyncio.TimeoutError as err:
            raise ArcticSpaConnectionError(
                f"Timeout connecting to Arctic Spa API: {url}"
            ) from err
        except aiohttp.ClientError as err:
            raise ArcticSpaConnectionError(
                f"Error connecting to Arctic Spa API: {err}"
            ) from err

    async def async_get_status(self) -> dict[str, Any]:
        """Get the current spa status."""
        result = await self._request("GET", "/spa/status")
        if result is None:
            raise ArcticSpaApiError("Empty response from status endpoint")
        return result

    async def async_set_lights(self, state: str) -> None:
        """Set the spa lights state ('on' or 'off')."""
        await self._request("PUT", "/spa/lights", {"state": state})

    async def async_set_pump(self, pump_id: int, state: str) -> None:
        """Set a pump state ('on', 'low', or 'off')."""
        await self._request("PUT", f"/spa/pumps/{pump_id}", {"state": state})

    async def async_set_temperature(self, setpoint_f: int) -> None:
        """Set the target temperature in Fahrenheit."""
        await self._request("PUT", "/spa/temperature", {"setpointF": setpoint_f})
