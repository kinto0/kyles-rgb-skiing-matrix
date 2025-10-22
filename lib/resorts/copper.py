from datetime import datetime
from lib.resorts.resort import Resort
import requests
from dotenv import load_dotenv
import os
from google.maps.routing_v2 import RoutesClient, ComputeRoutesRequest, Waypoint, Location, RouteTravelMode
from google.auth.credentials import AnonymousCredentials
from google.auth.transport.requests import Request
from lib.maps import time_to_drive_to

class Copper(Resort):
    def lift_open_percent(self) -> str:
        url = "https://api.coppercolorado.com/api/v1/dor/drupal/lifts"
        try:
            response = requests.get(url)
            response.raise_for_status()
            lifts = response.json()

            total_lifts = len(lifts)
            open_lifts = sum(1 for lift in lifts if lift.get("status") == "open")

            if total_lifts == 0:
                return "No lifts found."
            else:
                open_percentage = (open_lifts / total_lifts) * 100
                return f"Percentage of Lifts Open: {open_percentage:.2f}%"
        except requests.RequestException as e:
            return f"Error fetching lift data: {e}"
        except ValueError:
            return "Error parsing response data."

    def get_minutes_to_drive(self) -> str:
        destination_lat = 39.5020170751389  # Copper Mountain Resort, CO
        destination_lng = -106.14173211165492
        try:
            duration_minutes = time_to_drive_to(destination_lat, destination_lng)
            return f"{duration_minutes} min"
        except Exception as e:
            return f"Error calculating drive time: {e}"

    def get_recent_snowfall(self) -> str:
        return "0"