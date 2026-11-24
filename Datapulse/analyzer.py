
"""
DataPulse - Dataset Analyzer Module
"""

import pandas as pd
import numpy as np

from .statistics import DataStatistics
from .exceptions import EmptyDatasetError


class DataAnalyzer:
    """Perform complete dataset analysis."""

    def __init__(self, data):

        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a DataFrame.")

        if data.empty:
            raise EmptyDatasetError("Dataset is empty.")

        self.data = data.copy()

    def summary(self):

        numeric = self.data.select_dtypes(
            include=np.number
        )

        return {
            "total_rows": len(self.data),
            "total_columns": len(self.data.columns),
            "column_names": list(self.data.columns),
            "numeric_columns": list(numeric.columns),
            "categorical_columns": list(
                self.data.select_dtypes(
                    exclude=np.number
                ).columns
            ),
            "missing_values": int(
                self.data.isnull().sum().sum()
            ),
            "duplicate_rows": int(
                self.data.duplicated().sum()
            ),
            "memory_usage_bytes": int(
                self.data.memory_usage(deep=True).sum()
            )
        }

    def analyze_column(self, column):

        return DataStatistics.describe_column(
            self.data, column
        )

    def group_by(self, group_column, value_column,
                 operation="sum"):

        if group_column not in self.data.columns:
            raise ValueError("Group column not found.")

        if value_column not in self.data.columns:
            raise ValueError("Value column not found.")

        operations = {
            "sum": "sum",
            "mean": "mean",
            "median": "median",
            "count": "count",
            "max": "max",
            "min": "min"
        }

        if operation not in operations:
            raise ValueError("Unsupported grouping operation.")

        return self.data.groupby(
            group_column
        )[value_column].agg(
            operations[operation]
        ).sort_values(ascending=False)

    def top_records(self, column, count=5,
                    ascending=False):

        if column not in self.data.columns:
            raise ValueError("Column not found.")

        if count <= 0:
            raise ValueError("Count must be positive.")

        return self.data.nlargest(
            count, column
        ) if not ascending else self.data.nsmallest(
            count, column
        )

    def correlation(self):

        return DataStatistics.correlation_matrix(
            self.data
        )

    def get_data(self):

        return self.data.copy()
