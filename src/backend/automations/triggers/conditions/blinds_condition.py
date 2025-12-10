from logging import getLogger

from . import Condition

logger = getLogger(__name__)


class BlindsCondition(Condition):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.position: int | None = options.get("position") if options else None
    
    def evaluate(self, data: dict[str, object]) -> bool:
        if "position" in data and self.position is not None:
            logger.info(f"Evaluating BlindsCondition with condition position: {self.position} against device position: {data.get('position')}")
            self.evaluation = int(data.get("position")) == self.position

    def to_dict(self):
        dict = super().to_dict()
        dict["position"] = self.position

        return dict
