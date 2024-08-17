"""API Endpoints for the DVSA MOT History API."""

# Define base URL and endpoints
BASE_URL = "https://history.mot.api.gov.uk/v1/trade"

# Endpoints
VEHICLE_BY_REGISTRATION = "/vehicles/registration/{registration}"
VEHICLE_BY_VIN = "/vehicles/vin/{vin}"
BULK_DOWNLOAD = "/vehicles/bulk-download"


def build_url(endpoint: str, **kwargs: str) -> str:
    """Build a full URL from the base URL and endpoint with optional parameters."""
    return BASE_URL + endpoint.format(**kwargs)
