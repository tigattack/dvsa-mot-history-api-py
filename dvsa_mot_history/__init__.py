"""DVSA MOT History API wrapper"""

from .client import MOTHistory
from .models import (
    BulkDownloadResponse,
    CVSMotTest,
    DVANIMotTest,
    DVSAMotTest,
    ErrorResponse,
    FileResponse,
    MotTestDefect,
    MotTestType,
    NewRegVehicleResponse,
    VehicleWithMotResponse,
    VehicleResponseType,
)
from .enums import (
    MotTestDataSource,
    MotTestOdometerResultType,
    MotTestOdometerUnit,
    MotTestTestResult,
    VehicleHasOutstandingRecall,
)

__all__ = [
    "MOTHistory",
    "ErrorResponse",
    "MotTestDefect",
    "DVSAMotTest",
    "DVANIMotTest",
    "CVSMotTest",
    "MotTestType",
    "VehicleWithMotResponse",
    "NewRegVehicleResponse",
    "VehicleResponseType",
    "FileResponse",
    "BulkDownloadResponse",
    "MotTestTestResult",
    "MotTestOdometerUnit",
    "MotTestOdometerResultType",
    "MotTestDataSource",
    "VehicleHasOutstandingRecall",
]
