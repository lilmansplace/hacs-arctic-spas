"""Water heater platform for Arctic Spa."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_FILTER_STATUS,
    ATTR_SETPOINT_F,
    ATTR_TEMPERATURE_F,
    DOMAIN,
    MAX_TEMP_F,
    MIN_TEMP_F,
)
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Arctic Spa water heater."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ArcticSpaWaterHeater(coordinator)])


class ArcticSpaWaterHeater(ArcticSpaEntity, WaterHeaterEntity):
    """Representation of the Arctic Spa water heater."""

    _attr_name = "Hot Tub"
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
    _attr_min_temp = MIN_TEMP_F
    _attr_max_temp = MAX_TEMP_F
    _attr_icon = "mdi:hot-tub"

    def __init__(self, coordinator: ArcticSpaCoordinator) -> None:
        super().__init__(coordinator, "water_heater")

    @property
    def current_temperature(self) -> float | None:
        """Return the current water temperature."""
        value = self.coordinator.data.get(ATTR_TEMPERATURE_F)
        if value is not None:
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        value = self.coordinator.data.get(ATTR_SETPOINT_F)
        if value is not None:
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def current_operation(self) -> str | None:
        """Return the current filter/heating operation."""
        return self.coordinator.data.get(ATTR_FILTER_STATUS)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        temperature = kwargs.get("temperature")
        if temperature is not None:
            target = int(round(temperature))
            target = max(MIN_TEMP_F, min(MAX_TEMP_F, target))
            await self.coordinator.client.async_set_temperature(target)
            self.coordinator.data[ATTR_SETPOINT_F] = target
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()
