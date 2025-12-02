from logging import getLogger

from . import Hub

logger = getLogger(__name__)


class HueHub(Hub):
    def discover_devices(self):
        logger.info("Discovering devices through Hue protocol")
