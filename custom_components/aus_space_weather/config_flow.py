import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client, selector
from .const import DOMAIN, LOCATIONS

class SpaceWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for Australian Space Weather integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user inputs the API key and location."""
        errors = {}
        if user_input is not None:
            api_key = user_input["api_key"]
            location = user_input["location"]

            # Validate the API key with a test request
            session = aiohttp_client.async_get_clientsession(self.hass)
            try:
                response = await session.post(
                    "https://sws-data.sws.bom.gov.au/api/v1/get-a-index",
                    json={"api_key": api_key, "options": {"location": "Australian region"}},
                    timeout=10,
                )
                if response.status == 200:
                    data = await response.json()
                    if "data" in data:
                        # API key is valid, create the config entry
                        return self.async_create_entry(
                            title="Australian Space Weather",
                            data={"api_key": api_key, "location": location},
                        )
                    else:
                        errors["base"] = "invalid_api_key"
                else:
                    errors["base"] = "invalid_api_key"
            except Exception:
                errors["base"] = "unknown_error"

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("api_key"): str,
                vol.Required("location", default="Australian region"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=LOCATIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN
                    )
                ),
            }),
            errors=errors,
            description="Enter your API key. Register at https://sws-data.sws.bom.gov.au/register if needed.",
        )
