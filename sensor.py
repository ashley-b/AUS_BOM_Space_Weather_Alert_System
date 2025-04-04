from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from . import DEVICE_INFO

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
        if data and len(data) > 0:
            return data[0]["index"]
        return None

    @property
    def available(self):
        """Return if the sensor is available."""
        return self.coordinator.data.get(self._endpoint) is not None

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        data = self.coordinator.data.get(self._endpoint)
        if data and len(data) > 0:
            return {"valid_time": data[0]["valid_time"]}
        return {}
