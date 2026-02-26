"""Light platform for Arctic Spa."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ATTR_LIGHTS, DOMAIN
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa lights."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ArcticSpaLight(coordinator)])


class ArcticSpaLight(ArcticSpaEntity, LightEntity):
    """Representation of the Arctic Spa lights."""

    _attr_name = "Lights"
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(self, coordinator: ArcticSpaCoordinator) -> None:
        super().__init__(coordinator, "lights")

    @property
    def is_on(self) -> bool | None:
        """Return True if the lights are on."""
        value = self.coordinator.data.get(ATTR_LIGHTS)
        if value is None:
            return None
        return str(value).lower() == "on"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the lights."""
        await self.coordinator.client.async_set_lights("on")
        self.coordinator.data[ATTR_LIGHTS] = "on"
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the lights."""
        await self.coordinator.client.async_set_lights("off")
        self.coordinator.data[ATTR_LIGHTS] = "off"
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
