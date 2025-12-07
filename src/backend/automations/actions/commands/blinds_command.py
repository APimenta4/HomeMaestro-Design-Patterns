from . import Command


class BlindsCommand(Command):
    def __init__(self, device_id: int, feature_id: int, options: dict[str, object] | None = None):
        super().__init__(device_id, feature_id, options)
        self.position: int | None = self.options.get("position")

    def execute(self):
        pass

    def to_dict(self):
        dict = super().to_dict()
        dict["position"] = self.position

        return dict
