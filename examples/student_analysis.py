
"""
DataPulse - Student Performance Analysis Example
"""

import pandas as pd

from datapulse import (
    DataCleaner,
    DataValidator,
    DataAnalyzer,
    DataChartEngine,
    DataReport
)


def main():

    print("\n====== STUDENT PERFORMANCE ANALYSIS ======\n")

    # Sample student dataset
    data = pd.DataFrame({
        "Student": [
            "Asha", "Ravi", "Priya", "Kiran",
            "Neha", "Arjun", "Divya", "Rahul"
        ],

        "Python": [85, 72, 92, 65, 88, 78, 95, 70],

        "DBMS": [78, 80, 90, 60, 85, 75, 92, 68],

        "Mathematics": [90, 68, 95, 72, 82, 80, 98, 74],

        "Attendance": [95, 82, 98, 75, 90, 85, 96, 78]
    })

    # Calculate total marks
    data["Total"] = data[
        ["Python", "DBMS", "Mathematics"]
    ].sum(axis=1)

    data["Average"] = data[
        ["Python", "DBMS", "Mathematics"]
    ].mean(axis=1)

    # Clean data
    cleaner = DataCleaner(data)

    cleaner.remove_duplicates()

    clean_data = cleaner.get_cleaned_data()

    # Validate
    validator = DataValidator(clean_data)

    print("VALIDATION:")
    print(
        validator.validate(
            required_columns=[
                "Student",
                "Python",
                "DBMS",
                "Mathematics",
                "Attendance",
                "Total",
                "Average"
            ]
        )
    )

    # Analyze
    analyzer = DataAnalyzer(clean_data)

    print("\nSTUDENT DATA SUMMARY:")
    print(analyzer.summary())

    print("\nAVERAGE MARKS STATISTICS:")
    print(analyzer.analyze_column("Average"))

    print("\nTOP PERFORMING STUDENTS:")
    print(analyzer.top_records("Average", 3))

    # Generate charts
    charts = DataChartEngine(clean_data)

    charts.bar_chart(
        "Student",
        "Average",
        "output/student_performance.png",
        "Student Performance"
    )

    charts.histogram(
        "Average",
        "output/student_average_distribution.png",
        bins=5
    )

    charts.correlation_heatmap(
        "output/student_correlation.png"
    )

    # Export reports
    DataReport.export_csv(
        clean_data,
        "output/student_report.csv"
    )

    DataReport.export_pdf(
        clean_data,
        "output/student_report.pdf",
        "Student Performance Report"
    )

    print("\nSTUDENT REPORTS GENERATED SUCCESSFULLY")


if __name__ == "__main__":
    main()
