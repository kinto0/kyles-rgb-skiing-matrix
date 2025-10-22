from lib.resorts.copper import Copper

def main():
    resorts = [Copper()]  # Add other resorts here as needed

    for resort in resorts:
        print(f"Resort: {resort.__class__.__name__}")
        print(f"Lift Open Percentage: {resort.lift_open_percent()}")
        print(f"Minutes to Drive: {resort.get_minutes_to_drive()}")
        print("-" * 40)

if __name__ == "__main__":
    main()