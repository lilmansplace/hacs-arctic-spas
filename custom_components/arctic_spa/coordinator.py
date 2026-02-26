"""Data update coordinator for Arctic Spa."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ArcticSpaApiClient, ArcticSpaApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ArcticSpaCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage fetching Arctic Spa data."""

    def __init__(self, hass: HomeAssistant, client: ArcticSpaApiClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.client.async_get_status()
        except ArcticSpaApiError as err:
            raise UpdateFailed(f"Error communicating with Arctic Spa API: {err}") from err
