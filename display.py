#!/usr/bin/env python
import time
import asyncio
from datetime import datetime, timedelta
from matrix_api import Matrix, Color
from weather_api import get_weather, Weather
from lib.resorts import Breck, Copper, ABasin, Keystone
import signal, sys

matrix = Matrix()
text_color = Color(200, 200, 200)
no_color = Color(0, 0, 0)
half_seconds: int = 0

# Cached data
resort_stats = {}  # Cached resort stats

# List of resort instances
resorts = [Breck(), Copper(), ABasin(), Keystone()]

tasks = {}

async def update_resort_cache():
    """Update the cached resort stats every 15 minutes."""
    global resort_stats
    while True:
        for resort in resorts:
            resort_name = resort.__class__.__name__
            resort_stats[resort_name] = {
                "lift_percent": resort.lift_open_percent(),
                "snowfall": resort.get_recent_snowfall(),
                "drive_time": resort.get_minutes_to_drive(),
            }
        await asyncio.sleep(900)  # Update every 15 minutes

async def draw():
    global half_seconds, resorts, resort_stats
    half_seconds += 1

    # Clear the canvas by refreshing it
    matrix.tick()

    # Divide the space into sections for each resort
    section_height = 8  # Each resort gets 8 pixels of vertical space
    for i, resort in enumerate(resorts):
        y_offset = i * section_height
        resort_name = resort.__class__.__name__

        # Display resort name
        matrix.drawText(0, y_offset, text_color, resort_name)

        # Display cached resort stats
        if resort_name in resort_stats:
            stats = resort_stats[resort_name]
            matrix.drawText(0, y_offset + 6, text_color, f'Lifts: {stats["lift_percent"]}')
            matrix.drawText(0, y_offset + 12, text_color, f'Snow: {stats["snowfall"]}')
            matrix.drawText(0, y_offset + 18, text_color, f'Drive: {stats["drive_time"]}')

    # Refresh the matrix to display the updated content
    matrix.tick()

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
    matrix.drawText(0, 10, text_color, "loading")
    matrix.tick()

    await asyncio.gather(
        run_draw_loop(),
        update_resort_cache()
    )

if __name__ == '__main__':
    asyncio.run(main())
