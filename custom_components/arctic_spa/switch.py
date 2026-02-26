"""Switch platform for Arctic Spa."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_BLOWER1,
    ATTR_BLOWER2,
    ATTR_FILTER_STATUS,
    ATTR_FOGGER,
    ATTR_PUMP1,
    ATTR_PUMP2,
    ATTR_PUMP3,
    ATTR_PUMP4,
    ATTR_PUMP5,
    ATTR_SDS,
    ATTR_YESS,
    DOMAIN,
)
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ArcticSpaPumpDescription(SwitchEntityDescription):
    """Describe an Arctic Spa pump switch."""

    pump_id: int
    value_key: str
    on_state: str


@dataclass(frozen=True, kw_only=True)
class ArcticSpaFeatureDescription(SwitchEntityDescription):
    """Describe an Arctic Spa feature switch."""

    value_key: str
    feature: str
    off_states: tuple[str, ...] = ("off",)


PUMP_DESCRIPTIONS: tuple[ArcticSpaPumpDescription, ...] = (
    ArcticSpaPumpDescription(
        key="pump1",
        pump_id=1,
        value_key=ATTR_PUMP1,
        on_state="on",
        name="Pump 1",
        icon="mdi:pump",
    ),
    ArcticSpaPumpDescription(
        key="pump2",
        pump_id=2,
        value_key=ATTR_PUMP2,
        on_state="on",
        name="Pump 2",
        icon="mdi:pump",
    ),
    ArcticSpaPumpDescription(
        key="pump3",
        pump_id=3,
        value_key=ATTR_PUMP3,
        on_state="on",
        name="Pump 3",
        icon="mdi:pump",
    ),
    ArcticSpaPumpDescription(
        key="pump4",
        pump_id=4,
        value_key=ATTR_PUMP4,
        on_state="on",
        name="Pump 4",
        icon="mdi:pump",
    ),
    ArcticSpaPumpDescription(
        key="pump5",
        pump_id=5,
        value_key=ATTR_PUMP5,
        on_state="on",
        name="Pump 5",
        icon="mdi:pump",
    ),
)

FEATURE_DESCRIPTIONS: tuple[ArcticSpaFeatureDescription, ...] = (
    ArcticSpaFeatureDescription(
        key="blower1",
        value_key=ATTR_BLOWER1,
        feature="blowers/1",
        name="Blower 1",
        icon="mdi:fan",
    ),
    ArcticSpaFeatureDescription(
        key="blower2",
        value_key=ATTR_BLOWER2,
        feature="blowers/2",
        name="Blower 2",
        icon="mdi:fan",
    ),
    ArcticSpaFeatureDescription(
        key="sds",
        value_key=ATTR_SDS,
        feature="sds",
        name="SDS",
        icon="mdi:water-pump",
    ),
    ArcticSpaFeatureDescription(
        key="yess",
        value_key=ATTR_YESS,
        feature="yess",
        name="YESS",
        icon="mdi:lightning-bolt",
    ),
    ArcticSpaFeatureDescription(
        key="fogger",
        value_key=ATTR_FOGGER,
        feature="fogger",
        name="Fogger",
        icon="mdi:weather-fog",
    ),
    ArcticSpaFeatureDescription(
        key="filter",
        value_key=ATTR_FILTER_STATUS,
        feature="filter",
        name="Filter",
        icon="mdi:air-filter",
        off_states=("off", "idle"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa switches."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SwitchEntity] = []

    for description in PUMP_DESCRIPTIONS:
        if description.value_key in coordinator.data:
            entities.append(ArcticSpaPumpSwitch(coordinator, description))

    for description in FEATURE_DESCRIPTIONS:
        if description.value_key in coordinator.data:
            entities.append(ArcticSpaFeatureSwitch(coordinator, description))

    entities.append(ArcticSpaEasyModeSwitch(coordinator))

    async_add_entities(entities)


class ArcticSpaPumpSwitch(ArcticSpaEntity, SwitchEntity):
    """Representation of an Arctic Spa pump switch."""

    entity_description: ArcticSpaPumpDescription

    def __init__(
        self,
        coordinator: ArcticSpaCoordinator,
        description: ArcticSpaPumpDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return True if the pump is on."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        if value is None:
            return None
        return str(value).lower() not in ("off", "0", "false")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return pump speed as an extra attribute (relevant for pump 1)."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        if value is not None and str(value).lower() not in ("off", "0", "false"):
            return {"speed": str(value).lower()}
        return {}

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the pump."""
        desc = self.entity_description
        await self.coordinator.client.async_set_pump(desc.pump_id, desc.on_state)
        self.coordinator.data[desc.value_key] = desc.on_state
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the pump."""
        desc = self.entity_description
        await self.coordinator.client.async_set_pump(desc.pump_id, "off")
        self.coordinator.data[desc.value_key] = "off"
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()


class ArcticSpaFeatureSwitch(ArcticSpaEntity, SwitchEntity):
    """Representation of an Arctic Spa feature switch."""

    entity_description: ArcticSpaFeatureDescription

    def __init__(
        self,
        coordinator: ArcticSpaCoordinator,
        description: ArcticSpaFeatureDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return True if the feature is on."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        if value is None:
            return None
        return str(value).lower() not in self.entity_description.off_states

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the feature."""
        desc = self.entity_description
        await self.coordinator.client.async_set_feature(desc.feature, "on")
        self.coordinator.data[desc.value_key] = "on"
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the feature."""
        desc = self.entity_description
        await self.coordinator.client.async_set_feature(desc.feature, "off")
        self.coordinator.data[desc.value_key] = "off"
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()


class ArcticSpaEasyModeSwitch(ArcticSpaEntity, SwitchEntity):
    """Switch for spa easy mode (no state feedback from API)."""

    _attr_name = "Easy Mode"
    _attr_icon = "mdi:leaf"
    _attr_assumed_state = True

    def __init__(self, coordinator: ArcticSpaCoordinator) -> None:
        super().__init__(coordinator, "easymode")
        self._is_on: bool | None = None

    @property
    def is_on(self) -> bool | None:
        """Return assumed easy mode state."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on easy mode."""
        await self.coordinator.client.async_set_feature("easymode", "on")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off easy mode."""
        await self.coordinator.client.async_set_feature("easymode", "off")
        self._is_on = False
        self.async_write_ha_state()
