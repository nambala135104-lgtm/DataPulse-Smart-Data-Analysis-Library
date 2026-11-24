
"""
DataPulse - Data Cleaning Module

Provides automated data cleaning operations.
"""

import pandas as pd

from .exceptions import (
    DataCleaningError,
    DataPulseError
)


class DataCleaner:
    """Clean and prepare datasets for further analysis."""

    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a Pandas DataFrame.")

        if data.empty:
            raise DataPulseError("Cannot clean an empty dataset.")

        self.data = data.copy()
        self.cleaning_log = []

    def missing_values_summary(self):
        """Return missing value counts for every column."""
        return self.data.isnull().sum().to_dict()

    def remove_duplicates(self, keep="first"):
        """Remove duplicate records and return removal details."""

        try:
            before = len(self.data)

            self.data = self.data.drop_duplicates(
                keep=keep
            ).copy()

            removed = before - len(self.data)

            self.cleaning_log.append(
                f"Removed {removed} duplicate records."
            )

            return {
                "removed_duplicates": removed
            }

        except Exception as error:
            raise DataCleaningError(
                f"Duplicate removal failed: {error}"
            ) from error

    def fill_missing(self, strategy="auto", value=None):
        """
        Handle missing values using different strategies.
        Supported: auto, mean, median, mode, constant, drop.
        """

        if strategy not in (
            "auto", "mean", "median",
            "mode", "constant", "drop"
        ):
            raise ValueError("Unsupported cleaning strategy.")

        try:
            before = int(self.data.isnull().sum().sum())

            if strategy == "drop":
                self.data = self.data.dropna().copy()

            elif strategy == "constant":
                fill_value = 0 if value is None else value
                self.data = self.data.fillna(fill_value)

            elif strategy == "mode":
                for column in self.data.columns:
                    modes = self.data[column].mode(dropna=True)

                    if not modes.empty:
                        self.data[column] = self.data[column].fillna(
                            modes.iloc[0]
                        )

            else:
                numeric_columns = self.data.select_dtypes(
                    include="number"
                ).columns

                for column in self.data.columns:

                    if column in numeric_columns:
                        if strategy == "mean":
                            fill_value = self.data[column].mean()
                        else:
                            fill_value = self.data[column].median()

                    else:
                        modes = self.data[column].mode(dropna=True)

                        if modes.empty:
                            continue

                        fill_value = modes.iloc[0]

                    self.data[column] = self.data[column].fillna(
                        fill_value
                    )

            after = int(self.data.isnull().sum().sum())
            filled = before - after

            self.cleaning_log.append(
                f"Missing value strategy '{strategy}': "
                f"{filled} values handled."
            )

            return filled

        except Exception as error:
            raise DataCleaningError(
                f"Missing value handling failed: {error}"
            ) from error

    def handle_missing(self, strategy="mean", value=None):
        """Compatibility method for handling missing values."""

        self.fill_missing(strategy=strategy, value=value)
        return self.get_cleaned_data()

    def standardize_text(self):
        """Remove unnecessary spaces from text columns."""

        try:
            text_columns = self.data.select_dtypes(
                include=["object", "string"]
            ).columns

            for column in text_columns:
                self.data[column] = self.data[column].apply(
                    lambda item: item.strip()
                    if isinstance(item, str) else item
                )

            self.cleaning_log.append(
                "Text columns standardized."
            )

            return self.data.copy()

        except Exception as error:
            raise DataCleaningError(
                f"Text standardization failed: {error}"
            ) from error

    def remove_outliers(self, columns=None, factor=1.5):
        """Remove rows containing IQR-based numerical outliers."""

        if factor <= 0:
            raise ValueError("Factor must be greater than zero.")

        if columns is None:
            columns = list(
                self.data.select_dtypes(include="number").columns
            )

        if not columns:
            return 0

        for column in columns:
            if column not in self.data.columns:
                raise ValueError(
                    f"Column '{column}' does not exist."
                )

            if not pd.api.types.is_numeric_dtype(
                self.data[column]
            ):
                raise ValueError(
                    f"Column '{column}' must be numeric."
                )

        try:
            before = len(self.data)
            mask = pd.Series(True, index=self.data.index)

            for column in columns:
                q1 = self.data[column].quantile(0.25)
                q3 = self.data[column].quantile(0.75)

                iqr = q3 - q1

                lower = q1 - factor * iqr
                upper = q3 + factor * iqr

                mask &= self.data[column].between(
                    lower, upper
                )

            self.data = self.data.loc[mask].copy()

            removed = before - len(self.data)

            self.cleaning_log.append(
                f"Removed {removed} outlier records."
            )

            return removed

        except Exception as error:
            raise DataCleaningError(
                f"Outlier removal failed: {error}"
            ) from error

    def get_cleaned_data(self):
        """Return the cleaned dataset."""
        return self.data.copy()

    def get_cleaning_log(self):
        """Return the history of cleaning operations."""
        return self.cleaning_log.copy()
