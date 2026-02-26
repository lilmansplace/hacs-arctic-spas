"""Base entity for Arctic Spa."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_CONNECTED, DOMAIN
from .coordinator import ArcticSpaCoordinator


class ArcticSpaEntity(CoordinatorEntity[ArcticSpaCoordinator]):
    """Base class for Arctic Spa entities."""

    _attr_has_entity_name = True
    _check_spa_connected = True

    def __init__(self, coordinator: ArcticSpaCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Arctic Spa",
            manufacturer="Arctic Spas",
            model="Hot Tub",
        )

    @property
    def available(self) -> bool:
        """Return True if the entity is available."""
        if not super().available:
            return False
        if self._check_spa_connected:
            return bool(self.coordinator.data.get(ATTR_CONNECTED))
        return True
