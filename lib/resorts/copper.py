from lib.colors import IKON_COLOR
from lib.colors import Color
from datetime import datetime
from lib.resorts.resort import Resort
from dotenv import load_dotenv
import os
from lib.maps import time_to_drive_to
import requests

class Copper(Resort):
    def lift_open_percent(self) -> int:
        url = "https://api.coppercolorado.com/api/v1/dor/drupal/lifts"
        try:
            response = requests.get(url)  # Using requests to fetch data
            response.raise_for_status()  # Raise an exception for HTTP errors
            lifts = response.json()
            total_lifts = len(lifts)
            open_lifts = sum(1 for lift in lifts if lift.get("status") == "open")

            if total_lifts == 0:
                print("[copper] Total lifts is zero.")
                return 0
            else:
                return int((open_lifts / total_lifts) * 100)
        except Exception as e:
            print(f"[copper] Error fetching lift data: {e}")
            return 0

    def get_recent_snowfall(self) -> str:
        return "X"
    
    def get_short_name(self) -> str:
        return "Copr"

    def get_text_color(self) -> Color:
        return IKON_COLOR

    def get_coords(self) -> tuple[float, float]:
        return (39.50211136344817, -106.14069316085592)  # Alpine lot