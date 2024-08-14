"""Wrapper for DVSA MOT History API"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Type, Union

import aiohttp
from msal import ConfidentialClientApplication


class MotTestTestResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"


class MotTestOdometerUnit(Enum):
    MI = "MI"
    KM = "KM"
    NULL = None


class MotTestOdometerResultType(Enum):
    READ = "READ"
    UNREADABLE = "UNREADABLE"
    NO_ODOMETER = "NO_ODOMETER"


class MotTestDataSource(Enum):
    DVSA = "DVSA"
    DVA_NI = "DVA NI"
    CVS = "CVS"


class VehicleHasOutstandingRecall(Enum):
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"
    UNAVAILABLE = "Unavailable"


@dataclass
class ErrorResponse:
    """
    Error codes and response messages, where an error is returned.

    Attributes:
        status_code: The HTTP status code of the response.
        message: Additional details about the error.
        errors: A list of error codes identifying specific error types.
    """

    status_code: int
    message: str
    errors: Optional[List[str]]


@dataclass
class MotTestDefect:
    """
    Defects found during the MOT or annual test.

    Attributes:
        text: Description of the defect.
        type: The type of defect identified.
        dangerous: Indicates whether the defect is dangerous.
    """

    text: Optional[str]
    type: Optional[str]
    dangerous: Optional[bool]


@dataclass
class DVSAMotTest:
    """
    Test result information from DVSA (Driver and Vehicle Standards Agency, Great Britain).

    Attributes:
        completedDate: Date-time the test was completed.
        testResult: Result of the MOT test. Only Passed or Failed tests are included.
        expiryDate: Date the MOT test will expire.
        odometerValue: Odometer reading, if read.
        odometerUnit: Whether the odometer was read in miles or kilometres.
        odometerResultType: Whether or not the odometer was read during the MOT test.
        motTestNumber: 12-digit MOT test number.
        dataSource: Source of the MOT test data. In this case, DVSA.
        defects: Defects found during the MOT test.
    """

    completedDate: str
    testResult: MotTestTestResult
    expiryDate: Optional[str]
    odometerValue: Optional[int]
    odometerUnit: Optional[MotTestOdometerUnit]
    odometerResultType: MotTestOdometerResultType
    motTestNumber: Optional[int]
    dataSource: Literal[MotTestDataSource.DVSA]
    defects: List[MotTestDefect] = field(default_factory=list)

    def __post_init__(self):
        self.completedDate = parse_datetime(self.completedDate)
        self.expiryDate = parse_datetime(self.expiryDate)


@dataclass
class DVANIMotTest:
    """
    Test result data from DVA NI (Driver and Vehicle Agency, Northern Ireland).

    Attributes:
        completedDate: Date-time the test was completed.
        testResult: Result of the MOT test. Only Passed or Failed tests included.
        expiryDate: Date the MOT test will expire.
        odometerValue: Odometer reading, if read.
        odometerUnit: Whether the odometer was read in miles or kilometres.
        odometerResultType: Whether or not the odometer was read during the MOT test.
        motTestNumber: Identifier for the test.
        dataSource: Source of the MOT test data. In this case, DVA NI.
    """

    completedDate: str
    testResult: MotTestTestResult
    expiryDate: Optional[str]
    odometerValue: Optional[int]
    odometerUnit: Optional[MotTestOdometerUnit]
    odometerResultType: MotTestOdometerResultType
    motTestNumber: Optional[int]
    dataSource: Literal[MotTestDataSource.DVA_NI]

    def __post_init__(self):
        self.completedDate = parse_datetime(self.completedDate)
        self.expiryDate = parse_datetime(self.expiryDate)


@dataclass
class CVSMotTest:
    """
    Test result information from CVS (Commercial Vehicle Service).

    Attributes:
        completedDate: Date-time the test was completed.
        testResult: Result of the MOT test. Only Passed or Failed tests included.
        expiryDate: Date the MOT test will expire.
        odometerValue: Odometer reading, if read.
        odometerUnit: Whether the odometer was read in miles or kilometres.
        odometerResultType: Where the odometerResultType isn't available, set to NO_ODOMETER.
        motTestNumber: Test certificate number.
        location: Name of the Authorised Test Facility (ATF) where the test was conducted.
        dataSource: Source of the MOT test data. In this case, CVS.
        defects: Details of any defects found during the test.
    """

    completedDate: str
    testResult: MotTestTestResult
    expiryDate: Optional[str]
    odometerValue: Optional[int]
    odometerUnit: Optional[MotTestOdometerUnit]
    odometerResultType: MotTestOdometerResultType
    motTestNumber: Optional[int]
    location: Optional[str]
    dataSource: Literal[MotTestDataSource.CVS]
    defects: List[MotTestDefect] = field(default_factory=list)

    def __post_init__(self):
        self.completedDate = parse_datetime(self.completedDate)
        self.expiryDate = parse_datetime(self.expiryDate)


@dataclass
class VehicleWithMotResponse:
    """
    Vehicle data for vehicles with at least one MOT or annual test.

    Attributes:
        registration: Registration number of the vehicle.
        make: Name of the vehicle manufacturer.
        model: Model of the vehicle.
        firstUsedDate: Date the vehicle is first used in the United Kingdom.
        fuelType: The type of fuel the vehicle uses.
        primaryColour: Primary paint colour of the vehicle.
        registrationDate: Date the vehicle was first registered in the United Kingdom.
        manufactureDate: Date the vehicle was manufactured.
        engineSize: Engine cylinder capacity (cc) of the vehicle.
        hasOutstandingRecall: Status of outstanding recalls from the DVSA Recalls service.
        motTests: List of MOT or annual test results for the vehicle.
    """

    registration: Optional[str]
    make: Optional[str]
    model: Optional[str]
    firstUsedDate: Optional[str]
    fuelType: Optional[str]
    primaryColour: Optional[str]
    registrationDate: Optional[str]
    manufactureDate: Optional[str]
    engineSize: Optional[str]
    hasOutstandingRecall: VehicleHasOutstandingRecall
    motTests: List[Union[DVSAMotTest, DVANIMotTest, CVSMotTest]] = field(
        default_factory=list
    )

    def __post_init__(self):
        self.firstUsedDate = parse_datetime(self.firstUsedDate)
        self.registrationDate = parse_datetime(self.registrationDate)
        self.manufactureDate = parse_datetime(self.manufactureDate)


@dataclass
class NewRegVehicleResponse:
    """
    Vehicle data for newly registered vehicles.

    Attributes:
        registration: Registration number of the vehicle.
        make: Name of the vehicle manufacturer.
        model: Model of the vehicle.
        manufactureYear: The year the vehicle was manufactured.
        fuelType: The type of fuel the vehicle uses.
        primaryColour: Primary paint colour of the vehicle.
        registrationDate: Date the vehicle was first registered.
        manufactureDate: Date the vehicle was manufactured.
        motTestDueDate: Date the first MOT test is due.
        hasOutstandingRecall: Status of outstanding recalls from the DVSA Recalls service.
    """

    registration: Optional[str]
    make: Optional[str]
    model: Optional[str]
    manufactureYear: Optional[str]
    fuelType: Optional[str]
    primaryColour: Optional[str]
    registrationDate: Optional[str]
    manufactureDate: Optional[str]
    motTestDueDate: Optional[str]
    hasOutstandingRecall: VehicleHasOutstandingRecall

    def __post_init__(self):
        self.manufactureYear = parse_datetime(self.manufactureYear)
        self.registrationDate = parse_datetime(self.registrationDate)
        self.manufactureDate = parse_datetime(self.manufactureDate)
        self.motTestDueDate = parse_datetime(self.motTestDueDate)


@dataclass
class FileResponse:
    """
    File information from the bulk download service.

    Attributes:
        filename: Filename of the downloaded file.
        downloadUrl: Presigned URL for the related file. URL valid for 5 mins from generation.
        fileSize: Size of the ZIP file in bytes.
        fileCreatedOn: Date the file was created.
    """

    filename: str
    downloadUrl: str
    fileSize: int
    fileCreatedOn: str

    def __post_init__(self):
        self.fileCreatedOn = parse_datetime(self.fileCreatedOn)


@dataclass
class BulkDownloadResponse:
    """
    File information from the bulk download service.

    Attributes:
        bulk: Details about the bulk file.
        delta: Details about the delta files.
    """

    bulk: List[FileResponse]
    delta: List[FileResponse]


def parse_datetime(date_string: Optional[str]) -> Optional[datetime]:
    """Parse string to datetime object."""
    if date_string is None:
        return None
    if len(date_string) == 4:
        return datetime.strptime(date_string, "%Y")
    elif len(date_string) == 10:
        return datetime.strptime(date_string, "%Y-%m-%d")
    elif len(date_string) == 19:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    elif len(date_string) == 24 and date_string.endswith("Z"):
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    raise ValueError(f"Unexpected date string: {date_string}")


class MOTHistory:
    """Python SDK for DVSA MOT History API."""

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
        self.base_url = "https://history.mot.api.gov.uk/v1/trade"

        # Initialise the MSAL Confidential Client Application
        self.msal_app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
        )

    async def _get_access_token(self) -> str:
        """Obtain an access token using MSAL."""
        # acquire_token_for_client automatically checks cache before reaching out to the IDP
        token = self.msal_app.acquire_token_for_client(scopes=[self.scope])

        if not token.get("access_token"):
            raise Exception("Failed to obtain access token")

        return token["access_token"]

    async def _get_auth_headers(self) -> Dict[str, str]:
        """Generate the headers required for API requests."""
        token = await self._get_access_token()
        return {"Authorization": f"Bearer {token}", "X-API-Key": self.api_key}

    async def _make_api_request(
        self, endpoint: str
    ) -> Union[Dict[str, Any], ErrorResponse]:
        """Generic method to make API requests."""
        url = f"{self.base_url}{endpoint}"
        headers = await self._get_auth_headers()

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:  # noqa: PLR2004
                    return await response.json()
                elif response.status in {400, 404, 500}:
                    response_json = await response.json()
                    return ErrorResponse(
                        status_code=response.status,
                        message=response_json.get("message", "Unknown error"),
                        errors=response_json.get("errors"),
                    )
                response.raise_for_status()
                return ErrorResponse(
                    status_code=response.status, message="Unknown error", errors=None
                )

    @staticmethod
    async def _try_parse_dataclass(
        data: Dict[str, Any], dataclasse_types: List[Type]
    ) -> Any:
        """Try to parse data into one of the provided dataclasses."""
        for dataclass_type in dataclasse_types:
            try:
                return dataclass_type(**data)
            except TypeError:
                continue
        raise ValueError("Unexpected response format")

    async def _try_parse_mot_class(
        self, response_json
    ) -> List[Union[DVSAMotTest, DVANIMotTest, CVSMotTest]]:
        """Try to parse motTests attribute to applicable class."""
        mot_tests_data = response_json.get("motTests", [])
        parsed_mot_tests = []
        for mot_test in mot_tests_data:
            try:
                mot = await self._try_parse_dataclass(
                    mot_test, [DVSAMotTest, DVANIMotTest, CVSMotTest]
                )
                parsed_mot_tests.append(mot)
            except ValueError:
                raise ValueError(f"Unexpected response format for motTest: {mot_test}")
        return parsed_mot_tests

    async def get_vehicle_history_by_registration(
        self, registration: str
    ) -> Union[VehicleWithMotResponse, NewRegVehicleResponse, ErrorResponse]:
        """Get MOT history for a vehicle by registration."""
        endpoint = f"/vehicles/registration/{registration}"
        response_json = await self._make_api_request(endpoint)

        if isinstance(response_json, ErrorResponse):
            return response_json

        # Try to parse motTests attribute to applicable class
        if "motTests" in response_json:
            response_json["motTests"] = await self._try_parse_mot_class(response_json)

        # Try parsing the response into the possible dataclasses
        return await self._try_parse_dataclass(
            response_json, [VehicleWithMotResponse, NewRegVehicleResponse]
        )

    async def get_vehicle_history_by_vin(
        self, vin: str
    ) -> Union[VehicleWithMotResponse, NewRegVehicleResponse, ErrorResponse]:
        """Get MOT history for a vehicle by VIN."""
        endpoint = f"/vehicles/vin/{vin}"
        response_json = await self._make_api_request(endpoint)

        if isinstance(response_json, ErrorResponse):
            return response_json

        # Try to parse motTests attribute to applicable class
        if "motTests" in response_json:
            response_json["motTests"] = await self._try_parse_mot_class(response_json)

        # Try parsing the response into the possible dataclasses
        return await self._try_parse_dataclass(
            response_json, [VehicleWithMotResponse, NewRegVehicleResponse]
        )

    async def get_bulk_download(self) -> Union[BulkDownloadResponse, ErrorResponse]:
        """Get MOT history in bulk."""
        endpoint = "/vehicles/bulk-download"
        response_json = await self._make_api_request(endpoint)

        if isinstance(response_json, ErrorResponse):
            return response_json

        bulk = []
        for file in response_json.get("bulk", []):
            bulk.append(FileResponse(**file))

        delta = []
        for file in response_json.get("delta", []):
            delta.append(FileResponse(**file))

        return BulkDownloadResponse(bulk=bulk, delta=delta)
