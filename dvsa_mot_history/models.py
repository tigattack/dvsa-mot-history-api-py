"""Data models for the DVSA MOT History API"""

from datetime import date, datetime
from typing import Literal, Optional, TypeAlias, Union

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from .enums import (
    MotTestDataSource,
    MotTestOdometerResultType,
    MotTestOdometerUnit,
    MotTestTestResult,
    VehicleHasOutstandingRecall,
)


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

    completedDate: datetime
    testResult: MotTestTestResult
    expiryDate: Optional[date]
    odometerValue: Optional[int]
    odometerUnit: Optional[MotTestOdometerUnit]
    odometerResultType: MotTestOdometerResultType
    motTestNumber: Optional[str]
    dataSource: MotTestDataSource
    defects: list[MotTestDefect] = Field(default_factory=list)

    @field_validator("dataSource", mode="before")
    def validate_data_source(cls, v: str) -> Literal[MotTestDataSource.DVSA]:
        if v != MotTestDataSource.DVSA.value:
            raise ValueError(
                f"Invalid value '{v}' for dataSource. Expected '{MotTestDataSource.DVSA.value}'."
            )
        return MotTestDataSource.DVSA


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

    completedDate: datetime
    testResult: MotTestTestResult
    expiryDate: Optional[date]
    odometerValue: Optional[int]
    odometerUnit: Optional[MotTestOdometerUnit]
    odometerResultType: MotTestOdometerResultType
    motTestNumber: Optional[str]
    dataSource: MotTestDataSource

    @field_validator("dataSource", mode="before")
    def validate_data_source(cls, v: str) -> Literal[MotTestDataSource.DVA_NI]:
        if v != MotTestDataSource.DVA_NI.value:
            raise ValueError(
                f"Invalid value '{v}' for dataSource. Expected '{MotTestDataSource.DVA_NI.value}'."
            )
        return MotTestDataSource.DVA_NI


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

    completedDate: datetime
    testResult: MotTestTestResult
    expiryDate: Optional[date]
    odometerValue: Optional[int]
    odometerUnit: Optional[MotTestOdometerUnit]
    odometerResultType: MotTestOdometerResultType
    motTestNumber: Optional[str]
    location: Optional[str]
    dataSource: MotTestDataSource
    defects: list[MotTestDefect] = Field(default_factory=list)

    @field_validator("dataSource", mode="before")
    def validate_data_source(cls, v: str) -> Literal[MotTestDataSource.CVS]:
        if v != MotTestDataSource.CVS.value:
            raise ValueError(
                f"Invalid value '{v}' for dataSource. Expected '{MotTestDataSource.CVS.value}'."
            )
        return MotTestDataSource.CVS


MotTestType: TypeAlias = Union[DVSAMotTest, DVANIMotTest, CVSMotTest]


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
    firstUsedDate: Optional[date]
    fuelType: Optional[str]
    primaryColour: Optional[str]
    registrationDate: Optional[date]
    manufactureDate: Optional[date]
    engineSize: Optional[str]
    hasOutstandingRecall: VehicleHasOutstandingRecall
    motTests: list[MotTestType] = Field(default_factory=list)


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
    manufactureYear: Optional[int]
    fuelType: Optional[str]
    primaryColour: Optional[str]
    registrationDate: Optional[date]
    manufactureDate: Optional[date]
    motTestDueDate: Optional[date]
    hasOutstandingRecall: VehicleHasOutstandingRecall


VehicleResponseType: TypeAlias = Union[VehicleWithMotResponse, NewRegVehicleResponse]


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
    fileCreatedOn: date


@dataclass
class BulkDownloadResponse:
    """
    File information from the bulk download service.

    Attributes:
        bulk: Details about the bulk file.
        delta: Details about the delta files.
    """

    bulk: list[FileResponse]
    delta: list[FileResponse]
