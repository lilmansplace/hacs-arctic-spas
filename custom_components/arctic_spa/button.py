"""Button platform for Arctic Spa."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa buttons."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ArcticSpaBoostButton(coordinator)])


class ArcticSpaBoostButton(ArcticSpaEntity, ButtonEntity):
    """Button to activate spa boost mode."""

    _attr_name = "Boost"
    _attr_icon = "mdi:rocket-launch"

    def __init__(self, coordinator: ArcticSpaCoordinator) -> None:
        super().__init__(coordinator, "boost")

    async def async_press(self) -> None:
        """Activate boost mode."""
        await self.coordinator.client.async_activate_boost()
        await self.coordinator.async_request_refresh()
