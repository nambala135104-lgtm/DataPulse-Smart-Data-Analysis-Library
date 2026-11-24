
"""
DataPulse - Package Configuration
"""

from setuptools import setup, find_packages

setup(
    name="datapulse-library",
    version="1.0.0",

    description=(
        "A smart Python library for "
        "data analysis, cleaning and reporting"
    ),

    author="Bhargavi",

    packages=find_packages(),

    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "matplotlib>=3.7",
        "openpyxl>=3.1",
        "reportlab>=4.0"
    ],

    python_requires=">=3.9",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)
