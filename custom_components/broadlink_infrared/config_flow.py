"""Config flow for the Broadlink Infrared Emitter integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import CONF_BROADLINK_DEVICE_NAME, CONF_BROADLINK_ENTITY_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BroadlinkInfraredConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Broadlink Infrared Emitter."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step: select a Broadlink remote entity."""
        errors: dict[str, str] = {}

        if user_input is not None:
            entity_id = user_input[CONF_BROADLINK_ENTITY_ID]

            await self.async_set_unique_id(entity_id)
            self._abort_if_unique_id_configured()

            # Resolve friendly name from entity and device registries
            ent_reg = er.async_get(self.hass)
            dev_reg = dr.async_get(self.hass)
            ent_entry = ent_reg.async_get(entity_id)

            device_name = entity_id
            if ent_entry:
                if ent_entry.device_id:
                    dev_entry = dev_reg.async_get(ent_entry.device_id)
                    if dev_entry and dev_entry.name:
                        device_name = dev_entry.name
                elif ent_entry.name or ent_entry.original_name:
                    device_name = ent_entry.name or ent_entry.original_name

            return self.async_create_entry(
                title=f"{device_name} IR Emitter",
                data={
                    CONF_BROADLINK_ENTITY_ID: entity_id,
                    CONF_BROADLINK_DEVICE_NAME: device_name,
                },
            )

        broadlink_remotes = self._get_broadlink_remotes()

        if not broadlink_remotes:
            return self.async_abort(reason="no_broadlink_remotes")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_BROADLINK_ENTITY_ID): EntitySelector(
                        EntitySelectorConfig(
                            domain="remote",
                            include_entities=broadlink_remotes,
                        )
                    ),
                }
            ),
            errors=errors,
            description_placeholders={
                "count": str(len(broadlink_remotes)),
            },
        )

    def _get_broadlink_remotes(self) -> list[str]:
        """Find all remote entities that belong to the Broadlink integration."""
        ent_reg = er.async_get(self.hass)
        return [
            entity.entity_id
            for entity in ent_reg.entities.values()
            if entity.platform == "broadlink" and entity.domain == "remote"
        ]
