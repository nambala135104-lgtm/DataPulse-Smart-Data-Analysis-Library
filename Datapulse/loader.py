
"""
DataPulse - Dataset Loader Module

Loads datasets from CSV, Excel and JSON files.
"""

from pathlib import Path
import pandas as pd

from .exceptions import (
    DataFileNotFoundError,
    EmptyDatasetError,
    UnsupportedFormatError,
    DataPulseError
)


class DataLoader:
    """Load and manage datasets in different file formats."""

    SUPPORTED_FORMATS = {".csv", ".xlsx", ".json"}

    def __init__(self):
        self.data = None
        self.file_path = None

    def load(self, file_path):
        """Load a dataset and return it as a Pandas DataFrame."""

        path = Path(file_path)

        if not path.exists():
            raise DataFileNotFoundError(
                f"Dataset file not found: {path}"
            )

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise UnsupportedFormatError(
                f"Unsupported format: {path.suffix}"
            )

        try:
            if path.suffix.lower() == ".csv":
                dataset = pd.read_csv(path)

            elif path.suffix.lower() == ".xlsx":
                dataset = pd.read_excel(path)

            else:
                dataset = pd.read_json(path)

        except pd.errors.EmptyDataError:
            raise EmptyDatasetError(
                "The selected dataset file is empty."
            )

        except (pd.errors.ParserError, ValueError) as error:
            raise DataPulseError(
                f"Unable to read dataset: {error}"
            ) from error

        if dataset.empty:
            raise EmptyDatasetError(
                "The dataset contains no records."
            )

        self.data = dataset
        self.file_path = str(path.resolve())

        return self.data

    def get_info(self):
        """Return information about the loaded dataset."""

        return self.dataset_info()

    def preview(self, rows=5):
        """Display the first few rows of the loaded dataset."""

        if self.data is None:
            raise DataPulseError(
                "Load a dataset before requesting a preview."
            )

        if not isinstance(rows, int) or rows <= 0:
            raise ValueError("Rows must be a positive integer.")

        return self.data.head(rows)

    def dataset_info(self):
        """Return useful information about the loaded dataset."""

        if self.data is None:
            raise DataPulseError(
                "No dataset is currently loaded."
            )

        return {
            "file": self.file_path,
            "total_rows": self.data.shape[0],
            "total_columns": self.data.shape[1],
            "column_names": list(self.data.columns),
            "missing_values": int(self.data.isnull().sum().sum()),
            "duplicate_rows": int(self.data.duplicated().sum()),
            "memory_usage_kb": round(
                self.data.memory_usage(deep=True).sum() / 1024, 2
            )
        }
