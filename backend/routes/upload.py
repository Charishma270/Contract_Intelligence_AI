"""
Upload Route — /upload endpoint
================================
Production PDF upload + OCR ingestion pipeline.
"""

import os
import uuid
import logging

from fastapi import (
    APIRouter,
    File,
    UploadFile
)

from backend.schemas.contract_schema import (
    UploadResponse
)

from backend.services.tracking import (
    create_contract
)

from backend.utils.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    UnsupportedFileTypeError,
)

from ocr.ocr_pipeline import (
    process_contract
)

logger = logging.getLogger(
    "contract_ai.upload"
)

router = APIRouter()

UPLOAD_DIR = "uploads"

MAX_FILE_SIZE_MB = 20

MAX_FILE_SIZE_BYTES = (
    MAX_FILE_SIZE_MB
    * 1024
    * 1024
)

ALLOWED_CONTENT_TYPES = {
    "application/pdf"
}

ALLOWED_EXTENSIONS = {
    ".pdf"
}


@router.post(

    "/upload",

    response_model=UploadResponse,

    status_code=201
)

async def upload_contract(

    file: UploadFile = File(...)
):

    """
    Upload contract PDF
    → OCR extraction
    → chunking
    → embedding generation
    → FAISS indexing
    """

    # -----------------------------------------------------
    # Validate Extension
    # -----------------------------------------------------

    _, ext = os.path.splitext(
        file.filename or ""
    )

    if ext.lower() not in (
        ALLOWED_EXTENSIONS
    ):

        raise UnsupportedFileTypeError(

            f"Unsupported file type '{ext}'. "
            f"Only PDF files are accepted."
        )

    # -----------------------------------------------------
    # Validate MIME
    # -----------------------------------------------------

    if file.content_type not in (
        ALLOWED_CONTENT_TYPES
    ):

        raise UnsupportedFileTypeError(

            f"Unsupported content type "
            f"'{file.content_type}'. "
            f"Only application/pdf "
            f"is accepted."
        )

    # -----------------------------------------------------
    # Read File
    # -----------------------------------------------------

    contents = await file.read()

    if len(contents) == 0:

        raise EmptyFileError()

    if len(contents) > MAX_FILE_SIZE_BYTES:

        raise FileTooLargeError(

            size_mb=
            len(contents)
            /
            (1024 * 1024),

            max_mb=
            MAX_FILE_SIZE_MB
        )

    # -----------------------------------------------------
    # Validate PDF Signature
    # -----------------------------------------------------

    if not contents[:5] == b"%PDF-":

        raise UnsupportedFileTypeError(

            "File does not appear "
            "to be a valid PDF."
        )

    # -----------------------------------------------------
    # Save File
    # -----------------------------------------------------

    contract_id = str(uuid.uuid4())

    safe_filename = (
        f"{contract_id}{ext.lower()}"
    )

    file_path = os.path.join(

        UPLOAD_DIR,

        safe_filename
    )

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    with open(file_path, "wb") as f:

        f.write(contents)

    # -----------------------------------------------------
    # Track Upload
    # -----------------------------------------------------

    create_contract(

        contract_id=contract_id,

        filename=
        file.filename or "unknown.pdf",

        file_size_bytes=len(contents)
    )

    logger.info(

        f"Uploaded contract "
        f"{contract_id}"
    )

    # -----------------------------------------------------
    # OCR + RAG Ingestion
    # -----------------------------------------------------

    try:

        indexed_chunks = process_contract(

            pdf_path=file_path,

            contract_id=contract_id
        )

        logger.info(

            f"OCR ingestion completed "
            f"for contract {contract_id}"
        )

    except Exception as e:

        logger.error(

            f"OCR ingestion failed: {e}"
        )

        indexed_chunks = []

    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return UploadResponse(

        contract_id=contract_id,

        filename=
        file.filename or "unknown.pdf",

        status="uploaded",

        message=(
            f"File uploaded and "
            f"{len(indexed_chunks)} "
            f"chunks indexed successfully"
        ),

        file_size_bytes=len(contents),
    )