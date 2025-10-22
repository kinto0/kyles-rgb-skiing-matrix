from lib.resorts.resort import Resort
import requests
from bs4 import BeautifulSoup
from lib.maps import time_to_drive_to
import re
import json

class Breck(Resort):
    def lift_open_percent(self) -> str:
        return "TODO"

    def get_minute_to_drive(self) -> str:
        destination_lat = 39.48659659378005  # North gondola parking lot
        destination_lng = -106.04711242296264
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    def get_recent_snowfall(self) -> str:
        return 'todo'
