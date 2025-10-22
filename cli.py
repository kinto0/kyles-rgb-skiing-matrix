from lib.resorts.resort import Resort
import asyncio
from lib.resorts.breck import Breck
from lib.resorts import Copper, ABasin, Keystone

async def main():
    resorts = [Breck(), Copper(), ABasin(), Keystone()]  # Add other resorts here as needed


    for resort in resorts:
        print(f"Resort: {resort.__class__.__name__}")
        print(f"Lift Open Percentage: {resort.lift_open_percent()}")
        print(f"Minutes to Drive: {resort.get_minutes_to_drive()}")
        print(f"Recent Snowfall: {resort.get_recent_snowfall()")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())