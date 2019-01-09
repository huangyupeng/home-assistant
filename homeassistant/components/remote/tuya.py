"""
Support for Tuya IR remote.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/remote.tuya/
"""

from homeassistant.components.remote import (ENTITY_ID_FORMAT, RemoteDevice)
from homeassistant.components.tuya import DATA_TUYA, TuyaDevice

DEPENDENCIES = ['tuya']


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up Tuya IR remote platform."""
    if discovery_info is None:
        return
    tuya = hass.data[DATA_TUYA]
    dev_ids = discovery_info.get('dev_ids')
    devices = []
    for dev_id in dev_ids:
        device = tuya.get_device_by_id(dev_id)
        if device is None:
            continue
        devices.append(TuyaRemoteDevice(device))
    add_entities(devices)

class TuyaRemoteDevice(TuyaDevice, RemoteDevice):
    """Tuya IR remote devices."""

    def __init__(self, tuya):
        """Init Tuya fan device."""
        super().__init__(tuya)
        self.entity_id = ENTITY_ID_FORMAT.format(tuya.object_id())
        self._power = False

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._power

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._power = True
        self.tuya.send_command('turnOn')
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._power = False
        self.tuya.send_command('turnOff')
        self.schedule_update_ha_state()

    def send_command(self, command, **kwargs):
        """Send a command to one device."""
        for single_command in command:
            self.tuya.send_command(single_command)
