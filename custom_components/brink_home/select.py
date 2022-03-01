import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.brink_home import BrinkHomeDeviceEntity

from .const import (
    DATA_CLIENT,
    DATA_COORDINATOR,
    DOMAIN,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Brink Home sensor platform."""
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = []

    _LOGGER.info(f"entity data: {coordinator.data}")
    for deviceIndex, _ in enumerate(coordinator.data):
        entities.append(BrinkHomeVentilationSelectEntity(client, coordinator, deviceIndex, "ventilation"))
        entities.append(BrinkHomeModeSelectEntity(client, coordinator, deviceIndex, "mode"))

    _LOGGER.info(f"entity data: {entities}")
    async_add_entities(entities)


class BrinkHomeVentilationSelectEntity(BrinkHomeDeviceEntity, SelectEntity):

    async def async_select_option(self, option: str):
        mode = self.coordinator.data[self.device_index]["mode"]
        await self.client.set_ventilation_value(self.system_id, self.gateway_id, mode, self.data, option)

    @property
    def current_option(self) -> str:
        current_value = self.data["value"]
        return current_value

    @property
    def options(self) -> list[str]:
        """Return a set of selectable options."""
        values = []
        for value in self.data["values"]:
            values.append(value["value"])

        return values

    @property
    def name(self):
        return f"{self.coordinator.data[self.device_index]['name']} {self.device_info['name']}"

    @property
    def id(self):
        return f"{DOMAIN}_{self.name}_select"

    @property
    def unique_id(self):
        return self.id

    @property
    def icon(self) :
        """Return the icon to use in the frontend, if any."""
        return "mdi:hvac"


class BrinkHomeModeSelectEntity(BrinkHomeDeviceEntity, SelectEntity):

    async def async_select_option(self, option: str):
        await self.client.set_mode_value(self.system_id, self.gateway_id, self.data, option)

    @property
    def current_option(self) -> str:
        current_value = self.data["text"]
        return current_value

    @property
    def options(self) -> list[str]:
        """Return a set of selectable options."""
        values = []
        for value in self.data["values"]:
            values.append(value["text"])

        return values

    @property
    def name(self):
        return f"{self.coordinator.data[self.device_index]['name']} {self.device_info['name']}"

    @property
    def id(self):
        return f"{DOMAIN}_{self.name}_select"

    @property
    def unique_id(self):
        return self.id

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return "mdi:hvac"
