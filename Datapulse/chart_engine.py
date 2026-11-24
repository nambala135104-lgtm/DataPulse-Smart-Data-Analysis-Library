
"""
DataPulse - Chart Engine Module
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from .exceptions import DataPulseError


class DataChartEngine:
    """Generate visualizations from datasets."""

    def __init__(self, data):

        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a DataFrame.")

        self.data = data.copy()

    def _save(self, save_path, show=False):

        if save_path:
            path = Path(save_path)
            path.parent.mkdir(
                parents=True, exist_ok=True
            )

            plt.savefig(
                path,
                dpi=300,
                bbox_inches="tight"
            )

        if show:
            plt.show()

        result = str(save_path) if save_path else None

        plt.close()

        return result

    def bar_chart(self, x, y, save_path=None,
                  title="Bar Chart", show=False):

        if x not in self.data.columns or y not in self.data.columns:
            raise ValueError("Invalid chart columns.")

        plt.figure(figsize=(10, 6))
        plt.bar(self.data[x].astype(str), self.data[y])

        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.xticks(rotation=45)

        return self._save(save_path, show)

    def line_chart(self, x, y, save_path=None,
                   title="Line Chart", show=False):

        plt.figure(figsize=(10, 6))

        plt.plot(
            self.data[x],
            self.data[y],
            marker="o"
        )

        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.xticks(rotation=45)
        plt.grid(True)

        return self._save(save_path, show)

    def pie_chart(self, column, save_path=None,
                  title="Distribution", show=False):

        counts = self.data[column].value_counts()

        plt.figure(figsize=(8, 8))

        plt.pie(
            counts.values,
            labels=counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title(title)

        return self._save(save_path, show)

    def histogram(self, column, save_path=None,
                  bins=10, title="Histogram", show=False):

        plt.figure(figsize=(10, 6))

        plt.hist(
            self.data[column].dropna(),
            bins=bins,
            edgecolor="black"
        )

        plt.title(title)
        plt.xlabel(column)
        plt.ylabel("Frequency")

        return self._save(save_path, show)

    def correlation_heatmap(self, save_path=None,
                            title="Correlation Heatmap",
                            show=False):

        numeric = self.data.select_dtypes(
            include="number"
        )

        if numeric.empty:
            raise DataPulseError(
                "No numeric columns available."
            )

        correlation = numeric.corr()

        plt.figure(figsize=(9, 7))

        plt.imshow(
            correlation,
            cmap="coolwarm",
            interpolation="nearest"
        )

        plt.colorbar()

        plt.xticks(
            range(len(correlation.columns)),
            correlation.columns,
            rotation=45
        )

        plt.yticks(
            range(len(correlation.columns)),
            correlation.columns
        )

        plt.title(title)
        plt.tight_layout()

        return self._save(save_path, show)
