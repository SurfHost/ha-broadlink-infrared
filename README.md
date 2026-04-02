# Broadlink Infrared Emitter

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Custom Home Assistant integration that exposes Broadlink RM devices (RM4 Pro, RM4 Mini, etc.) as **infrared emitter entities** in the Home Assistant 2026.4 infrared platform.

## What does this do?

Home Assistant 2026.4 introduced a native `infrared` entity platform that decouples IR hardware from the devices they control. This integration bridges your existing Broadlink RM devices into that new system.

**Before (old way):** Manually learn IR codes, create scripts, call `remote.send_command` with device/command names. Lots of YAML.

**After (with this integration):** Your Broadlink RM4 Pro shows up as an IR emitter. Consumer integrations like `lg_infrared` or [Infrared Remote](https://github.com/SurfHost/ha-infrared-remote) can use it directly. Your TV appears as a proper `media_player` entity.

## Requirements

- Home Assistant **2026.4** or later
- The standard **Broadlink** integration already set up with your RM device(s)

## Installation via HACS

1. Open HACS in Home Assistant
2. Click the three dots in the top right and select **Custom repositories**
3. Add this repository URL and select **Integration** as category
4. Click **Download**
5. Restart Home Assistant

## Setup

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for **Broadlink Infrared Emitter**
3. Select which Broadlink remote entity to expose as an IR emitter
4. Done! Your Broadlink device is now available for consumer integrations

## Architecture

```
Consumer Integration (e.g., LG Infrared, Infrared Remote)
        |
        | sends InfraredCommand
        v
[HA infrared domain]
        |
        v
BroadlinkInfraredEntity (this integration)
        |
        | converts raw timings to Broadlink packet format
        v
Broadlink remote entity (standard broadlink integration)
        |
        | WiFi
        v
Broadlink RM4 Pro --> IR LED --> TV / AC / etc.
```

## Multiple devices

Set up this integration multiple times for multiple Broadlink RM devices (e.g., one per room).

## Limitations

- **Transmit only**: The new infrared platform currently supports sending only, not receiving/learning
- **Consumer integrations needed**: Works with integrations that use the new infrared platform (like `lg_infrared` or Infrared Remote)
- **Assumed state**: IR is one-way, so state tracking is assumed
