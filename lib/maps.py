from google.maps.routing_v2 import ComputeRoutesRequest, Waypoint, Location, RouteTravelMode
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials  # Remove AnonymousCredentials import
from google.maps.routing_v2 import RoutesClient
from google.maps.routing_v2.types import RouteMatrixElementCondition
from google.protobuf.field_mask_pb2 import FieldMask  # Import FieldMask
from google.api_core.client_options import ClientOptions  # Import ClientOptions
import os
from dotenv import load_dotenv

def time_to_drive_to(destination_lat: float, destination_lng: float) -> int:
    return 0
    load_dotenv()
    start_lat = float(os.getenv("START_LATITUDE", "0.0"))
    start_lng = float(os.getenv("START_LONGITUDE", "0.0"))
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY is not set in the environment variables.")

    # Set the required FieldMask in client_options
    client_options = ClientOptions(
        api_key=api_key,
    )
    client = RoutesClient(client_options=client_options)

    # Create the request
    request = ComputeRoutesRequest(
        origin=Waypoint(location=Location(lat_lng={"latitude": start_lat, "longitude": start_lng})),
        destination=Waypoint(location=Location(lat_lng={"latitude": destination_lat, "longitude": destination_lng})),
        travel_mode=RouteTravelMode.DRIVE
    )

    try:
        # Call the API with the field mask in metadata
        response = client.compute_routes(
            request=request,
            metadata=[("x-goog-fieldmask", "routes.duration")]
        )
        if not response.routes:
            raise ValueError("No routes found.")
        return int(response.routes[0].duration.seconds / 60)
    except Exception as e:
        raise RuntimeError(f"Error fetching route data: {e}")
