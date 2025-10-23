from lib.colors import IKON_COLOR
from lib.colors import Color
from lib.resorts.resort import Resort
import requests
from bs4 import BeautifulSoup
from lib.maps import time_to_drive_to

class ABasin(Resort):
    def lift_open_percent(self) -> str:
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
                        return "No lifts found."
                    else:
                        open_percentage = (open_lifts / total_lifts) * 100
                        return f"{open_percentage:.0f}%"
            
            return "No lift data found."
        except Exception as e:
            return f"Error fetching lift data: {e}"

    def get_minutes_to_drive(self) -> str:
        destination_lat = 39.63424085075325  # coordinates for Arapahoe Basin, CO
        destination_lng = -105.87140342042032
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    def get_recent_snowfall(self) -> str:
        url = "https://www.arapahoebasin.com/snow-report/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract snowfall data for the past 48 hours
            past_48hr = soup.find("div", class_="small-desc", text="Past 48HR").find_previous("h5", class_="big-number").text.strip()

            return f"{past_48hr}"
        except Exception as e:
            return f"Error fetching snowfall data: {e}"

    def get_short_name(self) -> str:
        return "ABay"

    def get_text_color(self) -> Color:
        return IKON_COLOR