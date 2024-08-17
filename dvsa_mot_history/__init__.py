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
    NewRegVehicleResponse,
    VehicleWithMotResponse,
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
    "VehicleWithMotResponse",
    "NewRegVehicleResponse",
    "FileResponse",
    "BulkDownloadResponse",
    "MotTestTestResult",
    "MotTestOdometerUnit",
    "MotTestOdometerResultType",
    "MotTestDataSource",
    "VehicleHasOutstandingRecall",
]
