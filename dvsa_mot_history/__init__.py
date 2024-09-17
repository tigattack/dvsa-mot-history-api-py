"""DVSA MOT History API wrapper"""

from .client import MOTHistory
from .enums import (
    MotTestDataSource,
    MotTestOdometerResultType,
    MotTestOdometerUnit,
    MotTestTestResult,
    VehicleHasOutstandingRecall,
)
from .errors import VehicleHistoryError
from .models import (
    BulkDownloadResponse,
    CVSMotTest,
    DVANIMotTest,
    DVSAMotTest,
    FileResponse,
    MotTestDefect,
    MotTestType,
    NewRegVehicleResponse,
    VehicleResponseType,
    VehicleWithMotResponse,
)

__all__ = [
    "BulkDownloadResponse",
    "CVSMotTest",
    "DVANIMotTest",
    "DVSAMotTest",
    "FileResponse",
    "MOTHistory",
    "MotTestDataSource",
    "MotTestDefect",
    "MotTestOdometerResultType",
    "MotTestOdometerUnit",
    "MotTestTestResult",
    "MotTestType",
    "NewRegVehicleResponse",
    "VehicleHasOutstandingRecall",
    "VehicleHistoryError",
    "VehicleResponseType",
    "VehicleWithMotResponse",
]
