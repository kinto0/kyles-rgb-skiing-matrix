from lib.weather_api import Weather
from lib.maps import time_to_drive_to
from lib.colors import Color
from abc import ABC, abstractmethod
from lib.weather_api import get_weather

class Resort(ABC):
    @abstractmethod
    def lift_open_percent(self) -> int:
        pass

    @abstractmethod
    def get_recent_snowfall(self) -> str:
        pass

    def get_minutes_to_drive(self) -> str:
        destination_lat, destination_lng = self.get_coords()
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    async def get_weather(self) -> Weather:
        destination_lat, destination_lng = self.get_coords()
        try:
            weather = await get_weather(destination_lat, destination_lng)
            return weather
        except Exception as e:
            print(f"[{self.get_short_name()}] Error fetching weather data: {e}")
            return Weather()


    @abstractmethod
    def get_short_name(self) -> str:
        """Should be 4 characters?"""
        pass

    @abstractmethod
    def get_text_color(self) -> Color:
        pass

    @abstractmethod
    def get_coords(self) -> tuple[float, float]:
        """Returns the latitude and longitude of the resort."""
        pass