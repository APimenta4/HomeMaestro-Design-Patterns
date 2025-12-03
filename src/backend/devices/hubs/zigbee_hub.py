from logging import getLogger

from devices import Protocol
from shared import HomeMaestro

from . import Hub

logger = getLogger(__name__)

home_maestro = HomeMaestro()


class ZigbeeHub(Hub):
    def discover_devices(self):
        logger.info(
            "Discovering devices through Zigbee protocol for hub '%s'", self.name
        )
        for device in home_maestro.unconnected_devices.copy():
            if device.protocol == Protocol.ZIGBEE:
                self.link_device(device)
                logger.info("Linked device '%s' to hub '%s'", device.name, self.name)
