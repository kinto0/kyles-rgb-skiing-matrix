from typing import Tuple
from lib.colors import IKON_COLOR
from lib.colors import Color
from lib.resorts.resort import Resort
import requests
from bs4 import BeautifulSoup
from lib.maps import time_to_drive_to

class ABasin(Resort):
    def lift_open_percent(self) -> int:
        url = "https://www.arapahoebasin.com/snow-report/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Locate the "Open Lifts" section
            summary_blocks = soup.find_all("div", class_="summary-box")
            for block in summary_blocks:
                if block.find("p") and "Open Lifts" in block.find("p").text:
                    # Extract the open and total lifts
                    lifts_text = block.find("h5").text.strip()
                    open_lifts, total_lifts = map(int, lifts_text.split("/"))
                    
                    if total_lifts == 0:
                        print("[abasin] Total lifts is zero.")
                        return 0
                    else:
                        return int((open_lifts / total_lifts) * 100)
            
            print("[abasin] Could not find lift data.")
            return 0
        except Exception as e:
            print(f"[abasin] error fetching lift data: {e}")
            return 0

    def get_recent_snowfall(self) -> int:
        url = "https://www.arapahoebasin.com/snow-report/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract snowfall data for the past 48 hours
            past_48hr = soup.find("div", class_="small-desc", text="Past 48HR").find_previous("h5", class_="big-number").text.strip()
            print(f"[abasin] Past 48HR snowfall: {past_48hr}")
            return int(past_48hr)
        except Exception as e:
            print(f"Error fetching snowfall data: {e}")
            return 0

    def get_short_name(self) -> str:
        return "ABay"

    def get_text_color(self) -> Color:
        return IKON_COLOR

    def get_coords(self) -> Tuple[float, float]:
        return (39.63424085075325, -105.87140342042032)  # Arapahoe Basin, CO