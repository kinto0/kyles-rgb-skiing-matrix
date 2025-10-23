from typing import Tuple
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

    def get_recent_snowfall(self) -> str:
        return 'X'

    def get_short_name(self) -> str:
        return 'Brck'

    def get_text_color(self) -> Color:
        return EPIC_COLOR

    def get_coords(self) -> Tuple[float, float]:
        return (39.48659659378005, -106.04711242296264) # north gondola parking lot