from lib.colors import EPIC_COLOR
from lib.colors import Color
from lib.resorts.resort import Resort
import requests
from bs4 import BeautifulSoup
from lib.maps import time_to_drive_to
import re
import json

class Breck(Resort):
    def lift_open_percent(self) -> int:
        return 0

    def get_minutes_to_drive(self) -> str:
        destination_lat = 39.48659659378005  # North gondola parking lot
        destination_lng = -106.04711242296264
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    def get_recent_snowfall(self) -> str:
        return 'X'

    def get_short_name(self) -> str:
        return 'Brck'

    def get_text_color(self) -> Color:
        return EPIC_COLOR