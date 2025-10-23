from matrix_api import Color
from matrix_api import EPIC_COLOR
from lib.resorts.resort import Resort
import requests
from bs4 import BeautifulSoup
import re
import json
from lib.maps import time_to_drive_to

class Keystone(Resort):
    def lift_open_percent(self) -> str:
        url = "https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract the embedded JavaScript containing lift data
            script_tags = soup.find_all("script")
            data_script = next(
                (script.string for script in script_tags if script.string and "TerrainStatusFeed" in script.string),
                None
            )
            if not data_script:
                return "No lift data found."

            # Extract the JSON object from the JavaScript
            match = re.search(r"TerrainStatusFeed\s*=\s*({.*?});", data_script, re.DOTALL)
            if not match:
                return "No lift data found."

            lift_data = json.loads(match.group(1)).get("Lifts", [])
            if not lift_data:
                return "No lift data found."

            # Calculate open lifts percentage
            total_lifts = len(lift_data)
            open_lifts = sum(1 for lift in lift_data if lift.get("Status") == 1)  # Status 1 = open

            if total_lifts == 0:
                return "No lifts found."
            else:
                open_percentage = (open_lifts / total_lifts) * 100
                return f"{open_percentage:.0f}%"
        except Exception as e:
            return f"Error fetching lift data: {e}"

    def get_minutes_to_drive(self) -> str:
        destination_lat = 39.60895859258185  # River Run Lot, Keystone Resort, CO
        destination_lng = -105.9438314730835
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    def get_recent_snowfall(self) -> str:
        return "TODO"

    def get_short_name(self) -> str:
        return "Kstn"

    def get_text_color(self) -> Color:
        return EPIC_COLOR