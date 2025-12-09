from logging import getLogger

from . import Condition

logger = getLogger(__name__)


class LockCondition(Condition):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.state: bool | None = options.get("state") if options else None

    def evaluate(self, data: dict[str, object]) -> bool:
        if "state" in data and self.state is not None:
            logger.info(f"Evaluating LockCondition with condition state: {self.state} against device state: {data.get("state")}")
            self.evaluation = float(data.get("state")) == self.state

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state

        return dict
