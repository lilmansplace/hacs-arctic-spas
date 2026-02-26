"""Switch platform for Arctic Spa."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ATTR_PUMP1, ATTR_PUMP2, ATTR_PUMP3, DOMAIN
from .coordinator import ArcticSpaCoordinator
from .entity import ArcticSpaEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ArcticSpaPumpDescription(SwitchEntityDescription):
    """Describe an Arctic Spa pump switch."""

    pump_id: int
    value_key: str
    on_state: str


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
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Arctic Spa pump switches."""
    coordinator: ArcticSpaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ArcticSpaPumpSwitch(coordinator, description)
        for description in PUMP_DESCRIPTIONS
    )


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
