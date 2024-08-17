"""Enumerations for DVSA MOT History API"""

from enum import Enum


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
