from logging import getLogger

from . import Hub

logger = getLogger(__name__)


class ZigbeeHub(Hub):
    def discover_devices(self):
        logger.info("Discovering devices through Zigbee protocol")
