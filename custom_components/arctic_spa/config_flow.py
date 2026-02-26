"""Config flow for Arctic Spa."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ArcticSpaApiClient, ArcticSpaAuthError, ArcticSpaConnectionError
from .const import CONF_API_KEY, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
    }
)


class ArcticSpaConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Arctic Spa."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            client = ArcticSpaApiClient(user_input[CONF_API_KEY], session)

            try:
                await client.async_get_status()
            except ArcticSpaAuthError:
                errors["base"] = "invalid_auth"
            except ArcticSpaConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception during setup")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    f"arctic_spa_{user_input[CONF_API_KEY][:8]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Arctic Spa",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
