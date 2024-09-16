from typing import Optional


class VehicleHistoryError(Exception):
    """Custom exception for vehicle history retrieval errors."""

    def __init__(
        self, status_code: int, message: str, errors: Optional[list[str]] = None
    ):
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code
        self.errors = errors
