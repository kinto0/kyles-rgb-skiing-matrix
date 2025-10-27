#!/usr/bin/env python
from typing import List
from typing import Dict
from dataclasses import dataclass
import time
import asyncio
from datetime import datetime, timedelta
from lib.matrix_api import Matrix
from lib.colors import Color
from lib.weather_api import get_weather, Weather
from lib.resorts import Breck, Copper, ABasin, Keystone
import signal, sys

matrix = Matrix()
text_color = Color(200, 200, 200)
no_color = Color(0, 0, 0)
half_seconds: int = 0

@dataclass
class ResortStats:
    lift_percent: int
    snowfall: int
    drive_time: str
    short_name: str
    text_color: Color
    weather: Weather

# Cached data
resort_stats: List[ResortStats] = []

# List of resort instances
resorts = [
    Breck(),
    Copper(),
    ABasin(),
    Keystone()
    ]

tasks = {}

refreshing = False

async def update_resort_cache():
    """Update the cached resort stats every 15 minutes."""
    global resort_stats, refreshing
    while True:
        resort_stats = []
        async def fetch_resort_stats(resort):
            return ResortStats(
                resort.lift_open_percent(),
                resort.get_recent_snowfall(),
                resort.get_minutes_to_drive(),
                resort.get_short_name(),
                resort.get_text_color(),
                await resort.get_weather(),
            )
        refreshing = True
        resort_stats = await asyncio.gather(*(fetch_resort_stats(resort) for resort in resorts))
        refreshing = False
        await asyncio.sleep(6000)  # Update every 100 minutes (for now while I'm working out the kinks)

async def draw():
    global half_seconds, resorts, resort_stats, refreshing
    half_seconds += 1

    # Clear the canvas by refreshing it
    matrix.tick()

    if refreshing:
        matrix.drawText(0, 10, text_color, "Refreshing...")
        return

    # Divide the space into sections for each resort
    section_height = 8  # Each resort gets 8 pixels of vertical space

    resort_stats.sort(key=lambda x: x.drive_time)
    for i, stat in enumerate(resort_stats):
        y_offset = 6 + i * section_height

        matrix.drawText(0, y_offset, stat.text_color, stat.short_name)

        # open percent line
        line_length = 16  # Full length of the line
        open_length = int(16 * (stat.lift_percent / 100))
        matrix.drawLine(0, y_offset, open_length, y_offset, Color(0, 255, 0))  # Green for open percent
        matrix.drawLine(open_length, y_offset, line_length, y_offset, Color(255, 0, 0))  # Red for remaining

        if stat.weather.icon_paths:
            icon_path = stat.weather.icon_paths[half_seconds % len(stat.weather.icon_paths)]
            matrix.setImage(icon_path, 17, y_offset - 5)
        matrix.drawText(24, y_offset, text_color, f'{stat.weather.current}°')

        matrix.drawText(37, y_offset, text_color, f'{stat.snowfall}"')
        matrix.drawText(45, y_offset, text_color, f'{stat.drive_time}')

async def run_draw_loop():
    """Continuously draw the display."""
    global tasks
    while True:
        tasks['draw'] = asyncio.gather(
            asyncio.sleep(.5),
            draw()
        )
        await tasks['draw']

def exit_gracefully(sig, frame):
    """Handle graceful shutdown."""
    global matrix, tasks
    print("exiting")
    [task.cancel() for _, task in tasks.items()]
    matrix.tick()
    sys.exit(0)

async def main():
    """Main entry point for the program."""
    global matrix, text_color

    signal.signal(signal.SIGINT, exit_gracefully)
    matrix.tick()

    await asyncio.gather(
        run_draw_loop(),
        update_resort_cache()
    )

if __name__ == '__main__':
    asyncio.run(main())
