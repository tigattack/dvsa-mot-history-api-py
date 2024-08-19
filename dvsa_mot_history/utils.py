"""Utility functions for the DVSA MOT History API"""

from typing import Any, Dict, List, Union

from .enums import MotTestDataSource
from .models import CVSMotTest, DVANIMotTest, DVSAMotTest


async def try_cast_mot_class(
    response_json: Dict[str, Any],
) -> List[Union[DVSAMotTest, DVANIMotTest, CVSMotTest]]:
    """Attempt to cast the 'motTests' attribute to the applicable MOT test class based on the 'dataSource' attribute."""
    mot_tests_data = response_json.get("motTests", [])
    parsed_mot_tests = []

    for mot_test in mot_tests_data:
        mot: Union[DVSAMotTest, DVANIMotTest, CVSMotTest]
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
