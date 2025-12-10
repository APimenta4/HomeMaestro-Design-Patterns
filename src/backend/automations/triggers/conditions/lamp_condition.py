from logging import getLogger

from . import Condition

logger = getLogger(__name__)


class LampCondition(Condition):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.state: bool | None = options.get("state") if options else None
        self.brightness: int | None = options.get("brightness") if options else None
    
    def evaluate(self, data: dict[str, object]) -> bool:
        if "state" in data and self.state is not None:
            logger.info(f"Evaluating LampCondition with condition state: {self.state} against device state: {data.get('state')}")
            self.evaluation = bool(data.get("state")) == self.state

        if "brightness" in data and self.brightness is not None:
            logger.info(f"Evaluating LampCondition with condition brightness: {self.brightness} against device brightness: {data.get('brightness')}")
            self.evaluation = int(data.get("brightness")) == self.brightness

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state
        dict["brightness"] = self.brightness

        return dict
