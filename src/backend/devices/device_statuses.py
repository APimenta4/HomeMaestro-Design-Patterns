from abc import ABC, abstractmethod

# DESIGN PATTERN: State
# makes code cleaner
# allows easily adding more device states in the future
# or change features, considering current requirements are vague
# approach using static methods enables an easy further refactoring if needed


class DeviceStatus(ABC):
    @staticmethod
    @abstractmethod
    def value() -> str:
        pass

    @staticmethod
    @abstractmethod
    def verify_can_execute() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def verify_can_obtain_status() -> bool:
        pass


class OnlineStatus(DeviceStatus):
    @staticmethod
    def value() -> str:
        return "online"

    @staticmethod
    def verify_can_execute() -> bool:
        return True

    @staticmethod
    def verify_can_obtain_status() -> bool:
        return True


class OfflineStatus(DeviceStatus):
    @staticmethod
    def value() -> str:
        return "offline"

    @staticmethod
    def verify_can_execute() -> bool:
        raise ValueError("Cannot execute features: Device is offline.")

    @staticmethod
    def verify_can_obtain_status() -> bool:
        raise ValueError("Cannot obtain status: Device is offline.")


class ErrorStatus(DeviceStatus):
    @staticmethod
    def value() -> str:
        return "error"

    @staticmethod
    def verify_can_execute() -> bool:
        raise ValueError("Cannot execute features: Device is in error state.")

    @staticmethod
    def verify_can_obtain_status() -> bool:
        return True
