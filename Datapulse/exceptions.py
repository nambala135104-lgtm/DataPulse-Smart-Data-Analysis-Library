
class DataPulseError(Exception):
    """Base exception for all DataPulse library errors."""
    pass


class DataFileNotFoundError(DataPulseError):
    """Raised when the requested dataset file is missing."""
    pass


class EmptyDatasetError(DataPulseError):
    """Raised when the loaded dataset contains no records."""
    pass


class InvalidColumnError(DataPulseError):
    """Raised when a required column is missing."""
    pass


class DataValidationError(DataPulseError):
    """Raised when dataset values are invalid."""
    pass


class UnsupportedFormatError(DataPulseError):
    """Raised when an unsupported file format is provided."""
    pass


class DataCleaningError(DataPulseError):
    """Raised when a data cleaning operation fails."""
    pass


class DataPulseExportError(DataPulseError):
    """Raised when exporting a report fails."""
    pass

class DataPulseLoadError(Exception):
    pass