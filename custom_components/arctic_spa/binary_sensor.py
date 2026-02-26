"""Binary sensor platform for Arctic Spa."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ATTR_CONNECTED, DOMAIN
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa binary sensors."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ArcticSpaConnectedSensor(coordinator)])


class ArcticSpaConnectedSensor(ArcticSpaEntity, BinarySensorEntity):
    """Binary sensor for spa connection status."""

    _attr_name = "Connected"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: ArcticSpaCoordinator) -> None:
        super().__init__(coordinator, "connected")

    @property
    def is_on(self) -> bool | None:
        """Return True if the spa is connected."""
        value = self.coordinator.data.get(ATTR_CONNECTED)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return None
