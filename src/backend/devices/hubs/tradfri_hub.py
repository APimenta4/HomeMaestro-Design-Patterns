from logging import getLogger

from . import Hub

logger = getLogger(__name__)


class TradfriHub(Hub):
    def discover_devices(self):
        logger.info("Discovering devices through Tradfri protocol")
