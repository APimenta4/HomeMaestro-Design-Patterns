from logging import getLogger

from shared import Identifiable, MQTTClient

from . import DeviceState
from .features import Feature

logger = getLogger(__name__)


class Device(Identifiable):
    def __init__(
        self, name: str, state: type[DeviceState], features: set[Feature] | None = None
    ):
        super().__init__(name)
        self.state = state
        self.features = features or set()

    def get_feature_by_id(self, feature_id: int) -> Feature | None:
        for feature in self.features:
            if feature.id == feature_id:
                return feature
        return None

    def execute_feature(
        self,
        feature_id: int,
    ):
        self.state.verify_can_execute()

        feature = self.get_feature_by_id(feature_id)
        if feature is None:
            raise ValueError(f"Feature with id '{feature_id}' does not exist on device")

        payload = feature.execute()
        # Overwrite payload while feature is not implemented yet
        # TODO: Remove following line
        payload = "that was a success!"
        MQTTClient().publish(f"{self.id}", payload)

    def get_feature_status(self, feature_id: int):
        self.state.verify_can_obtain_status()

        feature = self.get_feature_by_id(feature_id)
        if feature is None:
            raise ValueError(f"Feature with id '{feature_id}' does not exist on device")
        return feature.get_status()

    def to_dict(self) -> dict[str, object]:
        dict = super().to_dict()
        dict["status"] = self.state.value()
        dict["features"] = [feature.__class__.__name__ for feature in self.features]
        return dict

    def to_dict_deep(self) -> dict[str, object]:
        dict = self.to_dict()
        dict["features"] = [feature.to_dict() for feature in self.features]
        return dict
