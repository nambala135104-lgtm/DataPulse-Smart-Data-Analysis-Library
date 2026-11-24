
"""
DataPulse - Automated Unit Tests
"""

import unittest
import pandas as pd

from datapulse import (
    DataCleaner,
    DataValidator,
    DataAnalyzer,
    DataStatistics
)


class TestDataPulse(unittest.TestCase):

    def setUp(self):

        self.data = pd.DataFrame({
            "Name": ["A", "B", "C", "C"],
            "Marks": [80, 90, 70, 70],
            "Attendance": [90, 85, 95, 95]
        })

    def test_duplicate_removal(self):

        cleaner = DataCleaner(self.data)

        result = cleaner.remove_duplicates()

        self.assertEqual(
            result["removed_duplicates"], 1
        )

    def test_missing_value_handling(self):

        data = pd.DataFrame({
            "Marks": [80, None, 90]
        })

        cleaner = DataCleaner(data)

        cleaned = cleaner.handle_missing(
            strategy="mean"
        )

        self.assertEqual(
            cleaned["Marks"].isnull().sum(), 0
        )

    def test_validation(self):

        validator = DataValidator(self.data)

        result = validator.validate(
            required_columns=["Name", "Marks"]
        )

        self.assertTrue(result["valid"])

    def test_invalid_column(self):

        validator = DataValidator(self.data)

        result = validator.validate(
            required_columns=["Unknown"]
        )

        self.assertFalse(result["valid"])

        self.assertIn(
            "Unknown",
            result["missing_columns"]
        )

    def test_statistical_mean(self):

        result = DataStatistics.describe_column(
            self.data,
            "Marks"
        )

        self.assertEqual(result["mean"], 77.5)

    def test_dataset_summary(self):

        analyzer = DataAnalyzer(self.data)

        result = analyzer.summary()

        self.assertEqual(result["total_rows"], 4)

        self.assertEqual(result["total_columns"], 3)

    def test_group_analysis(self):

        analyzer = DataAnalyzer(self.data)

        result = analyzer.group_by(
            "Name",
            "Marks",
            "mean"
        )

        self.assertIn("A", result.index)


if __name__ == "__main__":

    unittest.main(verbosity=2)
