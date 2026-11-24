
"""
DataPulse - Statistical Analysis Module
"""

import pandas as pd
import numpy as np


class DataStatistics:
    """Advanced statistical calculations."""

    @staticmethod
    def describe_column(data, column):

        if column not in data.columns:
            raise ValueError(f"Column not found: {column}")

        if not pd.api.types.is_numeric_dtype(data[column]):
            raise TypeError("Column must contain numeric values.")

        series = data[column].dropna()

        if series.empty:
            raise ValueError("No valid numeric values.")

        mode_values = series.mode()

        return {
            "count": int(series.count()),
            "sum": float(series.sum()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "mode": mode_values.tolist(),
            "minimum": float(series.min()),
            "maximum": float(series.max()),
            "range": float(series.max() - series.min()),
            "variance": float(series.var()),
            "standard_deviation": float(series.std()),
            "q1": float(series.quantile(0.25)),
            "q3": float(series.quantile(0.75))
        }

    @staticmethod
    def correlation_matrix(data):
        numeric = data.select_dtypes(include=np.number)

        if numeric.empty:
            raise ValueError("No numeric columns available.")

        return numeric.corr()

    @staticmethod
    def frequency_counts(data, column):

        if column not in data.columns:
            raise ValueError(f"Column not found: {column}")

        return data[column].value_counts()

    @staticmethod
    def detect_outliers(data, column):

        series = data[column].dropna()

        if not pd.api.types.is_numeric_dtype(series):
            raise TypeError("Column must be numeric.")

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = series[
            (series < lower) | (series > upper)
        ]

        return {
            "lower_limit": float(lower),
            "upper_limit": float(upper),
            "outliers": outliers.tolist(),
            "outlier_count": len(outliers)
        }
