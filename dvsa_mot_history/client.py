"""Client for DVSA MOT History API"""

from typing import Any, Dict, Union

import aiohttp
from msal import ConfidentialClientApplication

from .api import BULK_DOWNLOAD, VEHICLE_BY_REGISTRATION, VEHICLE_BY_VIN, build_url
from .models import (
    BulkDownloadResponse,
    ErrorResponse,
    FileResponse,
    NewRegVehicleResponse,
    VehicleWithMotResponse,
)
from .utils import try_cast_mot_class


class MOTHistory:
    """DVSA MOT History API client"""

    def __init__(  # noqa: PLR0913
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        api_key: str,
        scope: str = "https://tapi.dvsa.gov.uk/.default",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.tenant_id = tenant_id
        self.api_key = api_key

        # Initialise the MSAL Confidential Client Application
        self.msal_app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
        )

    async def _get_access_token(self) -> str:
        """Obtain an access token using MSAL."""
        token = self.msal_app.acquire_token_for_client(scopes=[self.scope])

        if not token.get("access_token"):
            raise ValueError(
                "Failed to obtain credentials, access_token missing from response"
            )

        return str(token["access_token"])

    async def _get_auth_headers(self) -> Dict[str, str]:
        """Generate the headers required for API requests."""
        token = await self._get_access_token()
        return {"Authorization": f"Bearer {token}", "X-API-Key": self.api_key}

    async def _make_api_request(self, url: str) -> Union[Dict[str, Any], ErrorResponse]:
        """Generic method to make API requests."""
        headers = await self._get_auth_headers()

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:  # noqa: PLR2004
                    response_json_success: Dict[str, Any] = await response.json()
                    return response_json_success

                elif response.status in {400, 404, 500}:
                    response_json_err: Dict[str, Any] = await response.json()
                    return ErrorResponse(
                        status_code=response.status,
                        message=response_json_err.get("message", "Unknown error"),
                        errors=response_json_err.get("errors"),
                    )
                response.raise_for_status()
                return ErrorResponse(
                    status_code=response.status, message="Unknown error", errors=None
                )

    async def _process_vehicle_history_response(
        self, response_json: Dict[str, Any] | ErrorResponse
    ) -> Union[VehicleWithMotResponse, NewRegVehicleResponse, ErrorResponse]:
        """Process the vehicle history response."""
        if isinstance(response_json, ErrorResponse):
            return response_json

        if "motTests" in response_json:
            response_json["motTests"] = await try_cast_mot_class(response_json)
            return VehicleWithMotResponse(**response_json)
        elif "motTestDueDate" in response_json:
            return NewRegVehicleResponse(**response_json)

        raise ValueError("Unexpected response format")

    async def get_vehicle_history_by_registration(
        self, registration: str
    ) -> Union[VehicleWithMotResponse, NewRegVehicleResponse, ErrorResponse]:
        """Get MOT history for a vehicle by registration."""
        url = build_url(VEHICLE_BY_REGISTRATION, registration=registration)
        response_json = await self._make_api_request(url)
        return await self._process_vehicle_history_response(response_json)

    async def get_vehicle_history_by_vin(
        self, vin: str
    ) -> Union[VehicleWithMotResponse, NewRegVehicleResponse, ErrorResponse]:
        """Get MOT history for a vehicle by VIN."""
        url = build_url(VEHICLE_BY_VIN, vin=vin)
        response_json = await self._make_api_request(url)
        return await self._process_vehicle_history_response(response_json)

    async def get_bulk_download(self) -> Union[BulkDownloadResponse, ErrorResponse]:
        """Get MOT history in bulk."""
        url = build_url(BULK_DOWNLOAD)
        response_json = await self._make_api_request(url)

        if isinstance(response_json, ErrorResponse):
            return response_json

        if "bulk" in response_json and "delta" in response_json:
            bulk = [FileResponse(**file) for file in response_json["bulk"]]
            delta = [FileResponse(**file) for file in response_json["delta"]]
            return BulkDownloadResponse(bulk=bulk, delta=delta)

        return ErrorResponse(
            status_code=500, message="Unexpected response format", errors=None
        )
