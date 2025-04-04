# Australian Space Weather Alert System for Home Assistant

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)

This custom integration for Home Assistant delivers real-time space weather data from the Australian Bureau of Meteorologys Space Weather Services (SWS). It provides key indices such as A, K, and Dst, along with alerts, warnings, watches, and outlooks for magnetic and auroral activity.

## Features

- **Sensors**:
  - A Index
  - K Index (configurable for specific Australian locations)
  - Dst Index
- **Binary Sensors**:
  - Magnetic Alert
  - Magnetic Warning
  - Aurora Alert
  - Aurora Watch
  - Aurora Outlook

All data is sourced from the [Australian Space Weather Services API](https://sws-data.sws.bom.gov.au/api-docs).

## Installation

### Option 1: HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. Navigate to **HACS > Integrations > Explore & Add Integrations**.
3. Search for "Australian Space Weather" and click **Install**.
4. Restart Home Assistant.

### Option 2: Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/kcoffau/AUS_BOM_Space_Weather_Alert_System).
2. Extract the contents to the `custom_components/aus_space_weather/` directory in your Home Assistant configuration folder.
3. Restart Home Assistant.

## Configuration

1. After installation, go to **Settings > Devices & Services > Add Integration**.
2. Search for "Australian Space Weather" and select it.
3. Enter your API key (obtained from [SWS Registration](https://sws-data.sws.bom.gov.au/register)).
4. Select a location for the K Index (e.g., "Australian region", "Hobart", etc.).
5. Click **Submit** to finish setup.

### Obtaining an API Key

You’ll need an API key from the Australian Space Weather Services. Register for free at [https://sws-data.sws.bom.gov.au/register](https://sws-data.sws.bom.gov.au/register) to obtain your key.

## Usage

Once configured, the integration creates the following entities:

- **Sensors**:
  - `sensor.a_index`: Latest A index for the Australian region.
  - `sensor.k_index_<location>`: Latest K index for the chosen location (e.g., `sensor.k_index_hobart`).
  - `sensor.dst_index`: Latest Dst index for the Australian region.
- **Binary Sensors**:
  - `binary_sensor.magnetic_alert`: On if a magnetic alert is active.
  - `binary_sensor.magnetic_warning`: On if a magnetic warning is active.
  - `binary_sensor.aurora_alert`: On if an aurora alert is active.
  - `binary_sensor.aurora_watch`: On if an aurora watch is active.
  - `binary_sensor.aurora_outlook`: On if an aurora outlook is active.

These entities can be integrated into automations, dashboards, or notifications to track space weather conditions.

### Example Use Cases

- **Automation**: Send a notification when an aurora alert is triggered.
- **Dashboard**: Show the current K index on a Lovelace card to monitor geomagnetic activity.

## Data Update Frequency

The integration refreshes every 15 minutes to retrieve the latest data from the API.

## Acknowledgments

A heartfelt thank you to the [Australian Bureau of Meteorology (BOM)](https://www.bom.gov.au/) for providing the space weather data through their API. This integration relies on their excellent service to deliver valuable information to users.

## Support and Contributions

- **Issues**: Report bugs or suggest features on the [GitHub Issues page](https://github.com/kcoffau/AUS_BOM_Space_Weather_Alert_System/issues).
- **Contributions**: Pull requests are welcome! Check the contribution guidelines in the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/kcoffau/AUS_BOM_Space_Weather_Alert_System/blob/main/LICENSE) file for details.
