"""Utility functions to convert between HA InfraredCommand timings and Broadlink IR packet format.

Broadlink IR packet format (for IR, header byte 0x26):
  Byte 0:    0x26 (IR marker)
  Byte 1:    repeat count (0x00 = no repeat)
  Byte 2-3:  little-endian uint16, length of timing data in bytes
  Byte 4+:   timing data (variable length encoding, see below)
  Trailer:   0x0D 0x05

Timing data encoding:
  Each timing value is a duration in units of the Broadlink time quantum
  (~32.84 microseconds, exactly 269/8192 seconds).

  Values are alternating: mark (IR on), space (IR off), mark, space, ...

  Encoding per value:
    - If value <= 0xFF (fits in 1 byte): encoded as 1 byte
    - If value > 0xFF: encoded as 0x00 followed by 2 bytes big-endian uint16

The InfraredCommand.get_raw_timings() returns a list of Timing objects with
high_us (mark duration in microseconds) and low_us (space duration in microseconds).
"""

from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from .const import BROADLINK_IR_HEADER, BROADLINK_TICK_US, BROADLINK_TRAILER

if TYPE_CHECKING:
    from homeassistant.components.infrared import InfraredCommand


def us_to_broadlink_ticks(microseconds: int | float) -> int:
    """Convert microseconds to Broadlink timing ticks.

    The Broadlink time quantum is 269/8192 seconds (~32.84 us).
    """
    ticks = round(microseconds / BROADLINK_TICK_US)
    return max(1, ticks)  # minimum 1 tick


def encode_timing_value(ticks: int) -> bytes:
    """Encode a single timing value in Broadlink format.

    Values <= 255 are encoded as a single byte.
    Values > 255 are encoded as 0x00 followed by big-endian uint16.
    """
    if ticks <= 0xFF:
        return bytes([ticks])
    return b"\x00" + struct.pack(">H", min(ticks, 0xFFFF))


def infrared_command_to_broadlink_packet(command: InfraredCommand) -> bytes:
    """Convert an InfraredCommand to a Broadlink IR packet.

    Takes the raw timings from the InfraredCommand and builds a complete
    Broadlink IR packet ready to be sent via device.send_data().
    """
    raw_timings = command.get_raw_timings()

    # Build the timing data bytes
    timing_bytes = bytearray()
    for timing in raw_timings:
        # Mark (IR on) duration
        mark_ticks = us_to_broadlink_ticks(timing.high_us)
        timing_bytes.extend(encode_timing_value(mark_ticks))

        # Space (IR off) duration
        space_ticks = us_to_broadlink_ticks(timing.low_us)
        timing_bytes.extend(encode_timing_value(space_ticks))

    timing_length = len(timing_bytes)

    # Build the complete packet
    # Header: 0x26 (IR), repeat_count, length (LE uint16), timing data, trailer
    repeat_count = max(0, command.repeat_count)

    packet = bytearray()
    packet.append(BROADLINK_IR_HEADER)
    packet.append(repeat_count)
    packet.extend(struct.pack("<H", timing_length))
    packet.extend(timing_bytes)
    packet.extend(BROADLINK_TRAILER)

    return bytes(packet)
