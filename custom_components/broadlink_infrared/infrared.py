"""Infrared platform for Broadlink Infrared Emitter integration."""

from __future__ import annotations

import base64
import logging

from homeassistant.components.infrared import InfraredCommand, InfraredEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_BROADLINK_DEVICE_NAME, CONF_BROADLINK_ENTITY_ID, DOMAIN
from .converter import infrared_command_to_broadlink_packet

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Broadlink infrared emitter entity from a config entry."""
    broadlink_entity_id: str = config_entry.data[CONF_BROADLINK_ENTITY_ID]
    device_name: str = config_entry.data.get(
        CONF_BROADLINK_DEVICE_NAME, broadlink_entity_id
    )

    entity = BroadlinkInfraredEntity(
        config_entry=config_entry,
        broadlink_entity_id=broadlink_entity_id,
        device_name=device_name,
    )
    async_add_entities([entity])


class BroadlinkInfraredEntity(InfraredEntity):
    """Broadlink IR transmitter exposed as an InfraredEntity."""

    _attr_has_entity_name = True
    _attr_name = "IR Emitter"
    _attr_icon = "mdi:remote"

    def __init__(
        self,
        config_entry: ConfigEntry,
        broadlink_entity_id: str,
        device_name: str,
    ) -> None:
        """Initialize the Broadlink infrared entity."""
        self._broadlink_entity_id = broadlink_entity_id
        self._attr_unique_id = f"{config_entry.entry_id}_infrared"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=f"{device_name} IR Emitter",
            manufacturer="Broadlink",
            model="RM4 Pro",
            sw_version="0.3.0",
            via_device=None,
        )

    async def async_send_command(self, command: InfraredCommand) -> None:
        """Send an IR command via the Broadlink device."""
        _LOGGER.debug(
            "Sending IR command via Broadlink entity %s (modulation: %s kHz, repeats: %s)",
            self._broadlink_entity_id,
            command.modulation,
            command.repeat_count,
        )

        packet = infrared_command_to_broadlink_packet(command)
        b64_packet = base64.b64encode(packet).decode("ascii")

        await self.hass.services.async_call(
            "remote",
            "send_command",
            {
                "entity_id": self._broadlink_entity_id,
                "command": [f"b64:{b64_packet}"],
            },
            blocking=True,
        )

        _LOGGER.debug("IR command sent successfully via %s", self._broadlink_entity_id)
