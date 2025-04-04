import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from . import DEVICE_INFO

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        SpaceWeatherIndexSensor(coordinator, "get-a-index", "A Index"),
        SpaceWeatherIndexSensor(coordinator, "get-k-index", f"K Index ({coordinator.location})"),
        SpaceWeatherIndexSensor(coordinator, "get-dst-index", "Dst Index"),
    ]
    async_add_entities(sensors)

class SpaceWeatherIndexSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for space weather indices."""

    def __init__(self, coordinator, endpoint, name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._endpoint = endpoint
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{endpoint}"
        self._attr_device_info = DEVICE_INFO

    @property
    def state(self):
        """Return the sensor state."""
        data = self.coordinator.data.get(self._endpoint)
        if not data or not isinstance(data, list) or len(data) == 0:
            _LOGGER.error(f"No valid data for {self._endpoint}: {data}")
            return None
        first_item = data[0]
        if not isinstance(first_item, dict):
            _LOGGER.error(f"Unexpected data structure for {self._endpoint}: {first_item}")
            return None
        if "index" not in first_item:
            _LOGGER.error(f"No 'index' key in data for {self._endpoint}: {first_item}")
            return None
        return first_item["index"]

    @property
    def available(self):
        """Return if the sensor is available."""
        data = self.coordinator.data.get(self._endpoint)
        return data is not None and isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "index" in data[0]

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        data = self.coordinator.data.get(self._endpoint)
        if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            return {"valid_time": data[0].get("valid_time")}
        return {}
