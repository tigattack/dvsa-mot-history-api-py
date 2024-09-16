"""Utility functions for the DVSA MOT History API"""

from typing import Any

from .enums import MotTestDataSource
from .models import CVSMotTest, DVANIMotTest, DVSAMotTest, MotTestType


async def try_cast_mot_class(
    response_json: dict[str, Any],
) -> list[MotTestType]:
    """Attempt to cast the 'motTests' attribute to the applicable MOT test class based on the 'dataSource' attribute."""
    mot_tests_data = response_json.get("motTests", [])
    parsed_mot_tests = []

    for mot_test in mot_tests_data:
        mot: MotTestType
        data_source = mot_test.get("dataSource")

        if data_source == MotTestDataSource.DVSA.value:
            mot = DVSAMotTest(**mot_test)
        elif data_source == MotTestDataSource.DVA_NI.value:
            mot = DVANIMotTest(**mot_test)
        elif data_source == MotTestDataSource.CVS.value:
            mot = CVSMotTest(**mot_test)
        else:
            raise ValueError(
                f"Unexpected value '{data_source}' for dataSource in motTest: {mot_test}"
            )

        parsed_mot_tests.append(mot)

    return parsed_mot_tests
