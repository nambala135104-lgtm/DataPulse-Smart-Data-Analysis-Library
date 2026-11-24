
"""
DataPulse - Report Generation Module
"""

from pathlib import Path
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet

from .exceptions import DataPulseExportError


class DataReport:
    """Export dataset reports into multiple formats."""

    @staticmethod
    def export_csv(data, file_path):

        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            data.to_csv(path, index=False)

            return str(path)

        except Exception as error:
            raise DataPulseExportError(str(error)) from error

    @staticmethod
    def export_json(data, file_path):

        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            data.to_json(
                path,
                orient="records",
                indent=4,
                date_format="iso"
            )

            return str(path)

        except Exception as error:
            raise DataPulseExportError(str(error)) from error

    @staticmethod
    def export_pdf(data, file_path, title="DataPulse Analysis Report"):

        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            document = SimpleDocTemplate(
                str(path),
                pagesize=A4
            )

            styles = getSampleStyleSheet()

            elements = []

            elements.append(
                Paragraph(title, styles["Title"])
            )

            elements.append(Spacer(1, 20))

            summary = [
                ["Metric", "Value"],
                ["Total Rows", len(data)],
                ["Total Columns", len(data.columns)],
                ["Missing Values",
                 int(data.isnull().sum().sum())]
            ]

            table = Table(summary)

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.lightblue),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8)
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

            elements.append(
                Paragraph("Dataset Preview", styles["Heading2"])
            )

            preview = data.head(10).copy()
            preview = preview.fillna("")

            table_data = [
                [str(column) for column in preview.columns]
            ]

            for row in preview.itertuples(
                index=False, name=None
            ):
                table_data.append([
                    str(value)[:40] for value in row
                ])

            preview_table = Table(
                table_data,
                repeatRows=1
            )

            preview_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.lightblue),
                ("GRID", (0, 0), (-1, -1), 0.5,
                 colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("PADDING", (0, 0), (-1, -1), 5)
            ]))

            elements.append(preview_table)

            document.build(elements)

            return str(path)

        except Exception as error:
            raise DataPulseExportError(str(error)) from error
