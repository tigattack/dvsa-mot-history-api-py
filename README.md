# DVSA MOT History Python SDK

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tigattack/dvsa-mot-history-api-py/lint.yml?branch=main&style=for-the-badge&logo=github&label=lint)
![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/dvsa-mot-history?style=for-the-badge&logo=python&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdvsa-mot-history)
![PyPI - Version](https://img.shields.io/pypi/v/dvsa-mot-history?style=for-the-badge&logo=python&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdvsa-mot-history)

`dvsa_mot_history` is a Python SDK that provides a simple interface for interacting with the DVSA MOT History API, allowing retrieval of MOT history, test results, and bulk downloads for vehicles registered with DVSA, DVA Northern Ireland, or the Commercial Vehicle Service.

## Features

- **Retrieve Vehicle MOT History by Registration:** Fetch detailed MOT history using a vehicle's registration number.
- **Retrieve Vehicle MOT History by VIN:** Fetch detailed MOT history using a vehicle's VIN.
- **Bulk Download of MOT History Data:** Retrieve bulk MOT history data files for further processing.

## Installation

Install the package using pip:

```bash
pip install dvsa_mot_history
```

## Usage

### Initialisation

To use the `MOTHistory` class, you'll need the `client_id`, `client_secret`, `tenant_id`, and `api_key` credentials provided by the DVSA API service.

```python
from dvsa_mot_history import MOTHistory

mot_history = MOTHistory(
    client_id="your-client-id",
    client_secret="your-client-secret",
    tenant_id="your-tenant-id",
    api_key="your-api-key"
)
```

### Fetch MOT History by Registration

To fetch MOT history for a vehicle using its registration number:

```python
import asyncio
from dvsa_mot_history.errors import VehicleHistoryError

async def get_mot_history_by_registration():
    try:
        response = await mot_history.get_vehicle_history_by_registration("AB12CDE")
        print(f"Vehicle: {response.make} {response.model}")
        for test in response.motTests:
            print(f"Test Date: {test.completedDate}, Result: {test.testResult}")
    except VehicleHistoryError as e:
        print(f"Error: {e.message}")

asyncio.run(get_mot_history_by_registration())
```

### Fetch MOT History by VIN

To fetch MOT history for a vehicle using its VIN:

```python
async def get_mot_history_by_vin():
    try:
        response = await mot_history.get_vehicle_history_by_vin("12345678901234567")
        print(f"Vehicle: {response.make} {response.model}")
        for test in response.motTests:
            print(f"Test Date: {test.completedDate}, Result: {test.testResult}")
    except VehicleHistoryError as e:
        print(f"Error: {e.message}")

asyncio.run(get_mot_history_by_vin())
```

### Bulk Download of MOT History Data

To download bulk MOT history data:

```python
async def download_bulk_mot_history():
    try:
        response = await mot_history.get_bulk_download()
        for file in response.bulk:
            print(f"Bulk File: {file.filename}, URL: {file.downloadUrl}")
        for file in response.delta:
            print(f"Delta File: {file.filename}, URL: {file.downloadUrl}")
    except VehicleHistoryError as e:
        print(f"Error: {e.message}")

asyncio.run(download_bulk_mot_history())
```

## Classes and Data Structures

### MOT Test Classes

- `DVSAMotTest`
- `DVANIMotTest`
- `CVSMotTest`

These classes represent the MOT test results from their respective agencies, containing details such as the test result, odometer readings, defects, and more.

`MotTestType`: This is a type alias that encompasses the possible MOT test classes detailed above.

### Vehicle Response Classes

- `VehicleWithMotResponse`
- `NewRegVehicleResponse`

These classes encapsulate vehicle information, including the make, model, registration details, and a list of MOT tests.

`VehicleResponseType`: This is a type alias that encompasses the possible vehicle response classes detailed above.

### Error Handling

The `VehicleHistoryError` exception class handles errors returned by the API, providing details about the error, including the status code and message. The previous ErrorResponse class has been removed, and error handling is now done through exceptions.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
