"""Sensor platform for Arctic Spa."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity


@dataclass(frozen=True, kw_only=True)
class ArcticSpaSensorDescription(SensorEntityDescription):
    """Describe an Arctic Spa sensor."""

    value_key: str


SENSOR_DESCRIPTIONS: tuple[ArcticSpaSensorDescription, ...] = (
    ArcticSpaSensorDescription(
        key="temperature",
        value_key="temperatureF",
        translation_key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ArcticSpaSensorDescription(
        key="setpoint",
        value_key="setpointF",
        translation_key="setpoint",
        name="Set Point",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ArcticSpaSensorDescription(
        key="ph",
        value_key="ph",
        translation_key="ph_level",
        name="pH Level",
        native_unit_of_measurement="pH",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ph",
    ),
    ArcticSpaSensorDescription(
        key="ph_status",
        value_key="ph_status",
        translation_key="ph_status",
        name="pH Status",
        icon="mdi:ph",
    ),
    ArcticSpaSensorDescription(
        key="orp",
        value_key="orp",
        translation_key="orp_level",
        name="ORP Level",
        native_unit_of_measurement="mV",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-triangle-outline",
    ),
    ArcticSpaSensorDescription(
        key="orp_status",
        value_key="orp_status",
        translation_key="orp_status",
        name="ORP Status",
        icon="mdi:flash-triangle-outline",
    ),
    ArcticSpaSensorDescription(
        key="filter_status",
        value_key="filter_status",
        translation_key="filter_status",
        name="Filter Status",
        icon="mdi:air-filter",
    ),
    ArcticSpaSensorDescription(
        key="filter_duration",
        value_key="filter_duration",
        translation_key="filter_duration",
        name="Filter Duration",
        icon="mdi:timer-outline",
    ),
    ArcticSpaSensorDescription(
        key="filter_frequency",
        value_key="filter_frequency",
        translation_key="filter_frequency",
        name="Filter Frequency",
        icon="mdi:calendar-clock",
    ),
    ArcticSpaSensorDescription(
        key="filter_suspension",
        value_key="filter_suspension",
        translation_key="filter_suspension",
        name="Filter Suspension",
        icon="mdi:pause-circle-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa sensors."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ArcticSpaSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class ArcticSpaSensor(ArcticSpaEntity, SensorEntity):
    """Representation of an Arctic Spa sensor."""

    entity_description: ArcticSpaSensorDescription

    def __init__(
        self,
        coordinator: ArcticSpaCoordinator,
        description: ArcticSpaSensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self.coordinator.data.get(self.entity_description.value_key)
