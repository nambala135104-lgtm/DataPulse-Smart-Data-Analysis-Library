
"""
DataPulse - Data Validation Module

Provides dataset validation operations.
"""

import pandas as pd

from .exceptions import DataValidationError


class DataValidator:
    """Validate datasets and check column requirements."""

    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a Pandas DataFrame.")

        self.data = data.copy()

    def validate(self, required_columns=None):
        """Validate dataset columns and return results."""

        try:
            missing_columns = []

            if required_columns is not None:
                missing_columns = [
                    column for column in required_columns
                    if column not in self.data.columns
                ]

            valid = len(missing_columns) == 0

            return {
                "valid": valid,
                "missing_columns": missing_columns,
                "total_rows": len(self.data),
                "total_columns": len(self.data.columns),
                "message": (
                    "Dataset validation successful."
                    if valid
                    else f"Missing required columns: {missing_columns}"
                )
            }

        except Exception as error:
            raise DataValidationError(
                f"Dataset validation failed: {error}"
            ) from error

    def validate_columns(self, required_columns):
        return self.validate(required_columns)

    def validate_data(self):
        return self.validate()
