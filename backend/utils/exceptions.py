"""
Custom Exception Classes
=========================
Day 12: Centralized exception hierarchy for the Contract Intelligence AI backend.
All custom exceptions inherit from ContractAIError for easy global handling.
"""


class ContractAIError(Exception):
    """Base exception for all Contract Intelligence AI errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ContractNotFoundError(ContractAIError):
    """Raised when a contract_id does not exist in the database."""

    def __init__(self, contract_id: str):
        super().__init__(
            message=f"Contract '{contract_id}' not found.",
            status_code=404,
        )
        self.contract_id = contract_id


class ContractAlreadyFailedError(ContractAIError):
    """Raised when trying to process a contract that has already failed."""

    def __init__(self, contract_id: str, error_message: str = ""):
        detail = f"Contract '{contract_id}' previously failed"
        if error_message:
            detail += f": {error_message}"
        super().__init__(message=detail, status_code=400)
        self.contract_id = contract_id


class ContractNotAnalyzedError(ContractAIError):
    """Raised when querying a contract that hasn't been analyzed yet."""

    def __init__(self, contract_id: str):
        super().__init__(
            message=(
                f"Contract '{contract_id}' has not been analyzed yet. "
                f"Run POST /api/analyze/{contract_id} first."
            ),
            status_code=400,
        )
        self.contract_id = contract_id


class FileValidationError(ContractAIError):
    """Raised for file upload validation failures."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message=message, status_code=status_code)


class FileTooLargeError(FileValidationError):
    """Raised when an uploaded file exceeds the size limit."""

    def __init__(self, size_mb: float, max_mb: int):
        super().__init__(
            message=f"File too large ({size_mb:.1f} MB). Maximum allowed is {max_mb} MB.",
            status_code=413,
        )


class UnsupportedFileTypeError(FileValidationError):
    """Raised when file type or content type is not allowed."""

    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=415)


class EmptyFileError(FileValidationError):
    """Raised when an uploaded file is empty (0 bytes)."""

    def __init__(self):
        super().__init__(
            message="Uploaded file is empty (0 bytes).",
            status_code=400,
        )


class PipelineError(ContractAIError):
    """Raised when a pipeline stage fails."""

    def __init__(self, stage: str, contract_id: str, detail: str):
        super().__init__(
            message=f"Pipeline failed at stage '{stage}' for contract '{contract_id}': {detail}",
            status_code=500,
        )
        self.stage = stage
        self.contract_id = contract_id


class EmptyQueryError(ContractAIError):
    """Raised when a chat query is empty or whitespace-only."""

    def __init__(self):
        super().__init__(
            message="Query cannot be empty.",
            status_code=400,
        )


class InvalidContractIdError(ContractAIError):
    """Raised when a contract_id is not a valid UUID."""

    def __init__(self, contract_id: str):
        super().__init__(
            message=f"Invalid contract ID format: '{contract_id}'. Expected a valid UUID.",
            status_code=400,
        )
        self.contract_id = contract_id
