"""Binary sensor platform for Arctic Spa."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ATTR_CONNECTED, ATTR_SPABOY_CONNECTED, ATTR_SPABOY_PRODUCING, DOMAIN
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity


@dataclass(frozen=True, kw_only=True)
class ArcticSpaBinarySensorDescription(BinarySensorEntityDescription):
    """Describe an Arctic Spa binary sensor."""

    value_key: str


BINARY_SENSOR_DESCRIPTIONS: tuple[ArcticSpaBinarySensorDescription, ...] = (
    ArcticSpaBinarySensorDescription(
        key="connected",
        value_key=ATTR_CONNECTED,
        name="Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    ArcticSpaBinarySensorDescription(
        key="spaboy_connected",
        value_key=ATTR_SPABOY_CONNECTED,
        name="Spa Boy Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    ArcticSpaBinarySensorDescription(
        key="spaboy_producing",
        value_key=ATTR_SPABOY_PRODUCING,
        name="Spa Boy Producing",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa binary sensors."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ArcticSpaBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
        if description.value_key in coordinator.data
    )


class ArcticSpaBinarySensor(ArcticSpaEntity, BinarySensorEntity):
    """Representation of an Arctic Spa binary sensor."""

    entity_description: ArcticSpaBinarySensorDescription

    def __init__(
        self,
        coordinator: ArcticSpaCoordinator,
        description: ArcticSpaBinarySensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description
        if description.key == "connected":
            self._check_spa_connected = False

    @property
    def is_on(self) -> bool | None:
        """Return True if the binary sensor is on."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return None
