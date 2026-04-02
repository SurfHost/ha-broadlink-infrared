"""Constants for the Broadlink Infrared Emitter integration."""

DOMAIN = "broadlink_infrared"

CONF_BROADLINK_ENTITY_ID = "broadlink_entity_id"
CONF_BROADLINK_DEVICE_NAME = "broadlink_device_name"

BROADLINK_TICK_US = 269000 / 8192  # ~32.84 us per tick
BROADLINK_IR_HEADER = 0x26
BROADLINK_TRAILER = bytes([0x0D, 0x05])
