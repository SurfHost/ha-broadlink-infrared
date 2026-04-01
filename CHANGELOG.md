# Changelog

All notable changes to the Broadlink Infrared Emitter integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-01

### Added
- Integration icon in SVG, PNG, and PNG@2x formats
- Proper `DeviceInfo` so the device shows with correct name and manufacturer in HA
- Device name is resolved from the Broadlink device registry during setup
- Icon (`mdi:remote`) on the infrared emitter entity

### Fixed
- Device name showing as "None IR Emitter" due to missing `device_info` property
- "icon not available" on the integration page

## [0.1.0] - 2026-04-01

### Added
- Initial release
- `BroadlinkInfraredEntity` implementing the HA 2026.4 `InfraredEntity` base class
- Timing converter that translates `InfraredCommand` raw mark/space timings to Broadlink binary packet format (header 0x26, variable-length tick encoding, base64 output)
- Config flow that auto-discovers all Broadlink remote entities and lets the user select which one to expose as an IR emitter
- Sends IR commands via the existing Broadlink `remote.send_command` service using `b64:` prefix for raw packet data
- Support for multiple Broadlink devices (one emitter entity per RM device)
- English translations for the config flow

### Technical Details
- Broadlink time quantum: 269/8192 seconds (~32.84 us per tick)
- Timing values <= 255 encoded as 1 byte, > 255 as 0x00 + big-endian uint16
- Packet structure: `[0x26] [repeat_count] [length_le16] [timing_data] [0x0D 0x05]`
- Tested with Broadlink RM4 Pro and HA 2026.4.0
