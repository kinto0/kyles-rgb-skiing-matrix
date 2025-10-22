from datetime import datetime
from lib.resorts.resort import Resort
from dotenv import load_dotenv
import os
from lib.maps import time_to_drive_to
import requests

class Copper(Resort):
    def lift_open_percent(self) -> str:
        url = "https://api.coppercolorado.com/api/v1/dor/drupal/lifts"
        try:
            response = requests.get(url)  # Using requests to fetch data
            response.raise_for_status()  # Raise an exception for HTTP errors
            lifts = response.json()
            total_lifts = len(lifts)
            open_lifts = sum(1 for lift in lifts if lift.get("status") == "open")

            if total_lifts == 0:
                return "No lifts found."
            else:
                open_percentage = (open_lifts / total_lifts) * 100
                return f"{open_percentage:.2f}%"
        except Exception as e:
            return f"Error fetching lift data: {e}"

    def get_minutes_to_drive(self) -> str:
        destination_lat = 39.50211136344817  # Alpine lot
        destination_lng = -106.14069316085592
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    def get_recent_snowfall(self) -> str:
        return "TODO"