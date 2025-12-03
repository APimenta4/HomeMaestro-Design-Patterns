from logging import getLogger

from devices import Protocol
from shared import HomeMaestro

from . import Hub

logger = getLogger(__name__)

home_maestro = HomeMaestro()


class TradfriHub(Hub):
    def discover_devices(self):
        logger.info(
            "Discovering devices through Tradfri protocol for hub '%s'", self.name
        )
        for device in home_maestro.unconnected_devices.copy():
            if device.protocol == Protocol.ZWAVE:
                self.link_device(device)
                logger.info("Linked device '%s' to hub '%s'", device.name, self.name)
