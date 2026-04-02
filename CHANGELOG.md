# Changelog

All notable changes to the Broadlink Infrared Emitter integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-04-02

### Fixed
- Brand icons now in `brand/` directory with both `icon.png` and `logo.png` (HA 2026.3+ requirement)
- Removed SVG from brand folder (HA only supports PNG)

### Changed
- Updated documentation URL to GitHub repository
- Added `@SurfHost` as codeowner

## [0.2.0] - 2026-04-01

### Added
- Integration icon in PNG and PNG@2x formats
- Proper `DeviceInfo` so the device shows with correct name and manufacturer in HA
- Device name is resolved from the Broadlink device registry during setup
- Icon (`mdi:remote`) on the infrared emitter entity

### Fixed
- Device name showing as "None IR Emitter" due to missing `device_info` property

## [0.1.0] - 2026-04-01

### Added
- Initial release
- `BroadlinkInfraredEntity` implementing the HA 2026.4 `InfraredEntity` base class
- Timing converter: `InfraredCommand` raw timings to Broadlink binary packet format
- Config flow with auto-discovery of Broadlink remote entities
- Sends via existing Broadlink `remote.send_command` service using `b64:` prefix
- Support for multiple Broadlink devices
- Tested with Broadlink RM4 Pro and HA 2026.4.0
