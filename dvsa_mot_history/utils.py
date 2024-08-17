"""Utility functions for the DVSA MOT History API"""

from typing import Any, Dict, List, Type, Union

from .models import CVSMotTest, DVANIMotTest, DVSAMotTest


async def try_cast_dataclass(data: Dict[str, Any], dataclasses: List[Type[Any]]) -> Any:
    """Attempt to cast a dictionary into one of the provided dataclasses"""
    for dc in dataclasses:
        try:
            return dc(**data)
        except TypeError:
            continue
    raise ValueError("Unexpected response format")


async def try_cast_mot_class(
    response_json: Dict[str, Any],
) -> List[Union[DVSAMotTest, DVANIMotTest, CVSMotTest]]:
    """Attempt to cast the 'motTests' attribute to the applicable MOT test class"""
    mot_tests_data = response_json.get("motTests", [])
    parsed_mot_tests = []
    for mot_test in mot_tests_data:
        try:
            mot = await try_cast_dataclass(
                mot_test, [DVSAMotTest, DVANIMotTest, CVSMotTest]
            )
            parsed_mot_tests.append(mot)
        except ValueError as exc:
            raise ValueError(
                f"Unexpected response format for motTest: {mot_test}"
            ) from exc
    return parsed_mot_tests
