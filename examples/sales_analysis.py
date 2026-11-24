
"""
DataPulse - Retail Sales Analysis Example
"""

from pathlib import Path

from datapulse import (
    DataLoader,
    DataCleaner,
    DataValidator,
    DataAnalyzer,
    DataChartEngine,
    DataReport
)


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "datasets" / "retail_sales.csv"

OUTPUT_DIR = BASE_DIR / "output"


def main():

    print("\n========== DATAPULSE SALES ANALYSIS ==========\n")

    # 1. Load dataset
    loader = DataLoader()

    data = loader.load(DATA_PATH)

    print("DATASET LOADED SUCCESSFULLY")
    print(loader.get_info())

    # 2. Clean dataset
    cleaner = DataCleaner(data)

    cleaner.remove_duplicates()

    cleaner.handle_missing(strategy="median")

    clean_data = cleaner.get_cleaned_data()

    print("\nDATA CLEANING COMPLETED")

    # 3. Validate dataset
    validator = DataValidator(clean_data)

    validation = validator.validate(
        required_columns=[
            "Product",
            "Category",
            "Units_Sold",
            "Revenue",
            "Region"
        ]
    )

    print("\nVALIDATION RESULT:")
    print(validation)

    if not validation["valid"]:
        raise ValueError("Dataset validation failed.")

    # 4. Analyze dataset
    analyzer = DataAnalyzer(clean_data)

    print("\nDATASET SUMMARY:")
    print(analyzer.summary())

    print("\nREVENUE STATISTICS:")
    print(analyzer.analyze_column("Revenue"))

    print("\nREGION-WISE REVENUE:")
    print(
        analyzer.group_by(
            "Region",
            "Revenue",
            "sum"
        )
    )

    print("\nTOP 5 PRODUCTS BY REVENUE:")
    print(
        analyzer.top_records(
            "Revenue",
            count=5
        )
    )

    # 5. Generate charts
    charts = DataChartEngine(clean_data)

    OUTPUT_DIR.mkdir(exist_ok=True)

    charts.bar_chart(
        "Category",
        "Revenue",
        OUTPUT_DIR / "category_sales.png",
        "Category-wise Revenue"
    )

    charts.pie_chart(
        "Region",
        OUTPUT_DIR / "region_distribution.png",
        "Regional Distribution"
    )

    charts.histogram(
        "Revenue",
        OUTPUT_DIR / "revenue_distribution.png",
        bins=8
    )

    charts.correlation_heatmap(
        OUTPUT_DIR / "correlation.png"
    )

    print("\nCHARTS GENERATED SUCCESSFULLY")

    # 6. Export reports
    DataReport.export_csv(
        clean_data,
        OUTPUT_DIR / "cleaned_sales.csv"
    )

    DataReport.export_json(
        clean_data,
        OUTPUT_DIR / "sales_report.json"
    )

    DataReport.export_pdf(
        clean_data,
        OUTPUT_DIR / "sales_report.pdf",
        "DataPulse Retail Sales Report"
    )

    print("\nREPORTS GENERATED SUCCESSFULLY")

    print("\n========== ANALYSIS COMPLETED ==========\n")


if __name__ == "__main__":
    main()
