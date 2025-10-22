#!/usr/bin/env python
import time
import asyncio
from datetime import datetime, timedelta
from matrix_api import Matrix, Color
from weather_api import get_weather, Weather
import signal, sys

matrix = Matrix()
text_color = Color(200, 200, 200)
no_color = Color(0, 0, 0)
half_seconds: int = 0
current_weather = Weather()

tasks = {}

async def draw():
    global half_seconds, current_weather
    half_seconds += 1

    
    weather_y = 25
    # Draw weather
    matrix.drawText(9, weather_y + 5, text_color, f'{current_weather.current}°, {current_weather.low}°-{current_weather.high}°')

    if current_weather.icon_paths:
        icon_path = current_weather.icon_paths[half_seconds % len(current_weather.icon_paths)]
        matrix.setImage(icon_path, 2, weather_y)

    matrix.tick()

async def run_draw_loop():
    global tasks
    while True:
        tasks['draw'] = asyncio.gather(
                asyncio.sleep(.5),
                draw()
        )
        await tasks['draw']

async def run_weather_loop():
    async def update_weather():
        global current_weather
        current_weather = await get_weather()
    while True:
        tasks['weather'] = asyncio.gather(
                asyncio.sleep(3600),
                update_weather()
        )
        await tasks['weather']

def exit_gracefully(sig, frame):
    global matrix, tasks
    print("exiting")
    [task.cancel() for _, task in tasks.items()]
    matrix.tick()
    sys.exit(0)
    
async def main():
    global matrix, text_color

    signal.signal(signal.SIGINT, exit_gracefully)
    matrix.drawText(0, 10, text_color, "loading")
    matrix.tick()

    await asyncio.gather(
        run_draw_loop(),
        run_weather_loop()
    )

if __name__ == '__main__':
    asyncio.run(main())
