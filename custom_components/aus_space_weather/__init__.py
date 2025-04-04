import asyncio
from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Device information for grouping entities
DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "australian_space_weather")},
    name="Australian Space Weather",
    manufacturer="Bureau of Meteorology",
    model="Space Weather API",
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Australian Space Weather integration from a config entry."""
    api_key = entry.data["api_key"]
    location = entry.data["location"]

    # Create and initialize the data coordinator
    coordinator = SpaceWeatherDataCoordinator(hass, api_key, location)
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator in hass.data
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Forward setup to sensor and binary_sensor platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "binary_sensor"])

    return True

class SpaceWeatherDataCoordinator(DataUpdateCoordinator):
    """Coordinator to manage fetching data from the Space Weather API."""

    def __init__(self, hass, api_key, location):
        """Initialize the coordinator."""
        self.api_key = api_key
        self.location = location
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
        )

    async def _async_update_data(self):
        """Fetch data from all API endpoints in parallel."""
        session = async_get_clientsession(self.hass)

        # Use the user-selected location for all endpoints that require it
        endpoints = [
            ("get-a-index", {"location": self.location}),
            ("get-k-index", {"location": self.location}),
            ("get-dst-index", {"location": self.location}),
            ("get-mag-alert", {"location": self.location}),
            ("get-mag-warning", {"location": self.location}),
            ("get-aurora-alert", {"location": self.location}),
            ("get-aurora-watch", {"location": self.location}),
            ("get-aurora-outlook", {"location": self.location}),
        ]

        async def fetch(endpoint, options):
            """Fetch data from a single endpoint."""
            try
