from google.maps.routing_v2 import RoutesClient, ComputeRoutesRequest, Waypoint, Location, RouteTravelMode
from dotenv import load_dotenv
import os

def time_to_drive_to(destination_lat: float, destination_lng: float) -> int:
    load_dotenv()
    start_lat = float(os.getenv("START_LATITUDE"))
    start_lng = float(os.getenv("START_LONGITUDE"))
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    client = RoutesClient(credentials=None, client_options={"api_key": api_key})

    request = ComputeRoutesRequest(
        origin=Waypoint(location=Location(lat_lng={"latitude": start_lat, "longitude": start_lng})),
        destination=Waypoint(location=Location(lat_lng={"latitude": destination_lat, "longitude": destination_lng})),
        travel_mode=RouteTravelMode.DRIVE,
    )

    response = client.compute_routes(
        request=request,
        metadata=[("x-goog-fieldmask", "routes.duration,routes.legs.duration")]
    )
    duration = response.routes[0].legs[0].duration
    return duration.seconds // 60
