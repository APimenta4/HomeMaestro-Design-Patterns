from logging import getLogger

from . import Hub

logger = getLogger(__name__)


class ZWaveHub(Hub):
    def discover_devices(self):
        logger.info("Discovering devices through ZWave protocol")
