import asyncio
from lib.resorts.breck import Breck
from lib.resorts import Copper, ABasin, Keystone

async def main():
    resorts = [Copper()]  # Add other resorts here as needed

    async def fetch_resort_data(resort):
        return {
            "name": resort.__class__.__name__,
            "lift_open_percent": resort.lift_open_percent(),
            "minutes_to_drive": await resort.get_minutes_to_drive(),
            "recent_snowfall": resort.get_recent_snowfall(),
        }

    results = await asyncio.gather(*(fetch_resort_data(resort) for resort in resorts))

    for result in results:
        print(f"Resort: {result['name']}")
        print(f"Lift Open Percentage: {result['lift_open_percent']}")
        print(f"Minutes to Drive: {result['minutes_to_drive']}")
        print(f"Recent Snowfall: {result['recent_snowfall']}")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())