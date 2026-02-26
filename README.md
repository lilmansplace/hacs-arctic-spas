# Arctic Spa - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A custom Home Assistant integration for Arctic Spa hot tubs using the [myarcticspa.com](https://www.myarcticspa.com) cloud API.

## Features

- **Water Heater** - View current temperature and set target temperature
- **Light** - Turn spa lights on/off
- **Pump Switches** - Control pumps 1, 2, and 3
- **Sensors** - Monitor temperature, pH, ORP, filter status, and more
- **Binary Sensor** - Spa connectivity status
- **Services** - `arctic_spa.set_pump_speed` for pump 1 low-speed mode
- **Config Flow** - Set up entirely via the UI

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant.
2. Click the three dots menu in the top right and select **Custom repositories**.
3. Enter `https://github.com/lilmansplace/hacs-arctic-spas` and select **Integration** as the category.
4. Click **Add**, then find "Arctic Spa" in HACS and click **Install**.
5. Restart Home Assistant.
6. Go to **Settings > Devices & Services > Add Integration** and search for **Arctic Spa**.
7. Enter your API key.

### Manual

1. Copy the `custom_components/arctic_spa` folder to your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services > Add Integration** and search for **Arctic Spa**.
4. Enter your API key from [myarcticspa.com](https://www.myarcticspa.com).

## Configuration

The only required configuration is your Arctic Spa API key. You can obtain this from your [myarcticspa.com](https://www.myarcticspa.com) account.

## Entities Created

Entities marked with *(if enabled)* are only created when the spa reports that feature in its status.

### Controls

| Entity | Type | Description |
|--------|------|-------------|
| Arctic Spa Hot Tub | Water Heater | Current/target temperature control |
| Arctic Spa Lights | Light | On/off control |
| Arctic Spa Pump 1 | Switch | On/off (speed reported as attribute) |
| Arctic Spa Pump 2 | Switch | On/off control |
| Arctic Spa Pump 3 | Switch | On/off control |
| Arctic Spa Pump 4 | Switch | On/off control *(if enabled)* |
| Arctic Spa Pump 5 | Switch | On/off control *(if enabled)* |
| Arctic Spa Blower 1 | Switch | On/off control *(if enabled)* |
| Arctic Spa Blower 2 | Switch | On/off control *(if enabled)* |
| Arctic Spa SDS | Switch | Sanitize/Descale System on/off *(if enabled)* |
| Arctic Spa YESS | Switch | Energy saving system on/off *(if enabled)* |
| Arctic Spa Fogger | Switch | Fogger on/off *(if enabled)* |
| Arctic Spa Easy Mode | Switch | Easy mode on/off (assumed state) |
| Arctic Spa Filter | Switch | Filter on/off control |
| Arctic Spa Boost | Button | Activate boost mode |

### Sensors

| Entity | Type | Description |
|--------|------|-------------|
| Arctic Spa Temperature | Sensor | Current water temperature (°F) |
| Arctic Spa Set Point | Sensor | Target temperature (°F) |
| Arctic Spa pH Level | Sensor | Water pH level |
| Arctic Spa pH Status | Sensor | pH status (OK, CAUTION_HIGH, etc.) |
| Arctic Spa Chlorine Level | Sensor | Chlorine level via ORP (mV) |
| Arctic Spa Chlorine Status | Sensor | Chlorine status |
| Arctic Spa Filter Status | Sensor | Current filter status |
| Arctic Spa Filter Duration | Sensor | Filter cycle duration |
| Arctic Spa Filter Frequency | Sensor | Filter cycle frequency |
| Arctic Spa Filter Suspension | Sensor | Filter suspension status |
| Arctic Spa Errors | Sensor | Count of active error codes |
| Arctic Spa Last Online | Sensor | Timestamp of last successful connection |
| Arctic Spa Connected | Binary Sensor | API connectivity status |
| Arctic Spa Spa Boy Connected | Binary Sensor | Spa Boy® connection *(if enabled)* |
| Arctic Spa Spa Boy Producing | Binary Sensor | Spa Boy® producing *(if connected)* |

## Services

### `arctic_spa.set_pump_speed`

Set a pump to a specific speed. Useful for pump 1 which supports low-speed mode.

| Field | Description | Values |
|-------|-------------|--------|
| `pump_id` | Pump number | 1–5 |
| `speed` | Pump speed | `on`, `low`, `high`, `off` |

## Migrating from REST Configuration

If you were previously using REST sensors and commands for Arctic Spa, you can remove the following from your `configuration.yaml` once this integration is working:

- The `sensor` REST platform entry for Arctic Spa
- All `rest_command` entries for `spa_*`
- All `template` sensor entries for `Arctic Spa *`
- The `input_number.spa_set_temperature` helper (if no longer needed)

## Polling Interval

The integration polls the Arctic Spa API every 60 seconds.

## Troubleshooting

- **Cannot connect**: Verify your API key is correct and that you can access myarcticspa.com.
- **Entities unavailable**: The spa may be offline. Check the Connected binary sensor.
- **Stale data**: The API polls every 60 seconds. Wait for the next update cycle.
- **Check logs**: Look for `arctic_spa` entries in Home Assistant logs under **Settings > System > Logs**.
