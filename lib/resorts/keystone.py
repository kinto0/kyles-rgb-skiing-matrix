from typing import Tuple
from lib.colors import Color
from lib.colors import EPIC_COLOR
from lib.resorts.resort import Resort
import requests
from bs4 import BeautifulSoup
import re
import json
from lib.maps import time_to_drive_to

class Keystone(Resort):
    def lift_open_percent(self) -> int:
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
                print("[keystone] Could not find terrain status script.")
                return 0

            # Extract the JSON object from the JavaScript
            match = re.search(r"TerrainStatusFeed\s*=\s*({.*?});", data_script, re.DOTALL)
            if not match:
                print("[keystone] Could not find terrain status feed.")
                return 0

            lift_data = json.loads(match.group(1)).get("Lifts", [])
            if not lift_data:
                print("[keystone] No lift data found.")
                return 0

            # Calculate open lifts percentage
            total_lifts = len(lift_data)
            open_lifts = sum(1 for lift in lift_data if lift.get("Status") == 1)  # Status 1 = open

            if total_lifts == 0:
                print("[keystone] Total lifts is zero.")
                return 0
            else:
                return int((open_lifts / total_lifts) * 100)
        except Exception as e:
            print(f"[keystone] Error fetching lift data: {e}")
            return 0

    def get_recent_snowfall(self) -> str:
        return "X"

    def get_short_name(self) -> str:
        return "Kstn"

    def get_text_color(self) -> Color:
        return EPIC_COLOR

    def get_coords(self) -> Tuple[float, float]:
        return (39.60895859258185, -105.9438314730835) # river run lot