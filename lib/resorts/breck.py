from typing import Tuple
from lib.colors import EPIC_COLOR
from lib.colors import Color
from lib.resorts.resort import Resort
from lib.onthesnow import fetch_and_parse, extract_section, parse_ratio, extract_last_table_value

ONTHESNOW_URL = "https://www.onthesnow.com/colorado/breckenridge/skireport"
class Breck(Resort):
    def lift_open_percent(self) -> int:
        soup = fetch_and_parse(ONTHESNOW_URL)
        lifts_section = extract_section(soup, "lifts_section")

        # Extract the "Lifts Open" text (e.g., "3/35 open")
        lifts_text = lifts_section.find("div", class_="styles_metric__z_U_F").text.strip()
        open_lifts, total_lifts = parse_ratio(lifts_text)

        # Calculate the percentage of open lifts
        return int((open_lifts / total_lifts) * 100) if total_lifts > 0 else 0

    def get_recent_snowfall(self) -> int:
        soup = fetch_and_parse(ONTHESNOW_URL)
        snowfall_table = soup.find("table", class_="styles_snowChart__S2PJB")
        if not snowfall_table:
            print("Could not find the snowfall table on the page.")
            return 0

        # Extract the most recent snowfall value
        recent_snowfall = extract_last_table_value(
            snowfall_table, "snowfall_cell", "snowfall_value"
        )
        return int(recent_snowfall.replace("\"", ""))

    def get_short_name(self) -> str:
        return 'Brck'

    def get_text_color(self) -> Color:
        return EPIC_COLOR

    def get_coords(self) -> Tuple[float, float]:
        return (39.48659659378005, -106.04711242296264) # north gondola parking lot

    def get_expected_minutes_to_drive(self) -> int:
        return 18