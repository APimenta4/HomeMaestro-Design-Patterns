from logging import getLogger

from . import Condition

logger = getLogger(__name__)


class TemperatureCondition(Condition):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.temperature: float | None = options.get("temperature") if options else None

    def evaluate(self, data: dict[str, object]) -> bool:
        if "temperature" in data and self.temperature is not None:
            logger.info(f"Evaluating TemperatureCondition with condition temperature: {self.temperature} against device temperature: {data.get("temperature")}")
            self.evaluation = float(data.get("temperature")) == self.temperature

    def to_dict(self):
        dict = super().to_dict()
        dict["temperature"] = self.temperature

        return dict
