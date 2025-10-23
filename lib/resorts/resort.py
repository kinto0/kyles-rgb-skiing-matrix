from abc import ABC, abstractmethod

class Resort(ABC):
    @abstractmethod
    def lift_open_percent(self) -> str:
        pass

    @abstractmethod
    def get_recent_snowfall(self) -> str:
        pass

    @abstractmethod
    def get_minutes_to_drive(self) -> str:
        pass

    @abstractmethod
    def get_short_name(self) -> str:
        """Should be 4 characters?"""
        pass