from . import Feature
from typing import TypedDict, Optional


class LockParameters(TypedDict, total=False):
    state: bool


class LockFeature(Feature):
    def __init__(self, name: str, options: Optional[LockParameters] = None):
        super().__init__(name, options)
        self.state = options.get("state", False)  # A lock is locked (True) or unlocked (False)

    def execute(self, options: Optional[LockParameters] = None):
        if options:
            if "state" in options:
                self.state = bool(options.get("state", self.state))
                if self.options:
                    self.options["state"] = self.state
        return f"Lock state set to {'Locked' if self.state else 'Unlocked'}"

    def get_status(self):
        return {"state": self.state}

    def to_dict(self):
        dict = super().to_dict()
        dict["state"] = self.state
        return dict
