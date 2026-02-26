"""The Arctic Spa integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ArcticSpaApiClient
from .const import CONF_API_KEY, DOMAIN
from .coordinator import ArcticSpaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.WATER_HEATER,
]

SERVICE_SET_PUMP_SPEED = "set_pump_speed"
SERVICE_SET_PUMP_SPEED_SCHEMA = vol.Schema(
    {
        vol.Required("pump_id"): vol.All(int, vol.Range(min=1, max=5)),
        vol.Required("speed"): vol.In(["on", "low", "high", "off"]),
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Arctic Spa from a config entry."""
    session = async_get_clientsession(hass)
    client = ArcticSpaApiClient(entry.data[CONF_API_KEY], session)

    coordinator = ArcticSpaCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    async def handle_set_pump_speed(call: ServiceCall) -> None:
        """Handle the set_pump_speed service call."""
        pump_id = call.data["pump_id"]
        speed = call.data["speed"]
        for coord in hass.data[DOMAIN].values():
            await coord.client.async_set_pump(pump_id, speed)
            await coord.async_request_refresh()

    if not hass.services.has_service(DOMAIN, SERVICE_SET_PUMP_SPEED):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SET_PUMP_SPEED,
            handle_set_pump_speed,
            schema=SERVICE_SET_PUMP_SPEED_SCHEMA,
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_SET_PUMP_SPEED)
    return unload_ok
