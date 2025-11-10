from typing import Tuple, Dict
import requests
from bs4 import BeautifulSoup
import re

CLASS_NAMES: Dict[str, str] = {
    "lifts_section": "styles_metricsBox__3HVsE",
    "lifts_text": "styles_metric__z_U_F",
    "snowfall_table": "styles_snowChart__S2PJB",
    "snowfall_cell": "styles_cell__jT46b",
    "snowfall_value": "styles_snow__5Bl0_",
}

def fetch_and_parse(url: str) -> BeautifulSoup:
    """Fetch the HTML content of a URL and parse it with BeautifulSoup."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}, status code: {response.status_code}")
    return BeautifulSoup(response.text, "html.parser")

def extract_section(soup: BeautifulSoup, class_name_key: str) -> BeautifulSoup:
    """Extract a specific section of the page by class name key."""
    class_name = CLASS_NAMES.get(class_name_key)
    if not class_name:
        raise Exception(f"Class name key '{class_name_key}' not found in CLASS_NAMES.")
    section = soup.find("div", class_=class_name)
    if not section:
        raise Exception(f"Could not find the section with class '{class_name}' on the page.")
    return section

def parse_ratio(text: str) -> Tuple[int, int]:
    """Parse a ratio string (e.g., '3/35') into two integers."""
    match = re.match(r"(\d+)/(\d+)", text)
    if not match:
        raise Exception(f"Failed to parse ratio from text: '{text}'")
    return map(int, match.groups())

def extract_last_table_value(table: BeautifulSoup, cell_class_key: str, value_class_key: str) -> str:
    """Extract the last value from a table column."""
    cell_class = CLASS_NAMES.get(cell_class_key)
    value_class = CLASS_NAMES.get(value_class_key)
    if not cell_class or not value_class:
        raise Exception(f"Class name keys '{cell_class_key}' or '{value_class_key}' not found in CLASS_NAMES.")
    cells = table.find_all("td", class_=cell_class)
    if not cells:
        raise Exception(f"No cells found with class '{cell_class}' in the table.")
    last_cell = cells[-1]
    value = last_cell.find("span", class_=value_class)
    if not value:
        raise Exception(f"No value found with class '{value_class}' in the last cell.")
    return value.text.strip()
