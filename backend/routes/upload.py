"""
Upload Route — /upload endpoint
================================
Day 4: PDF upload with validation.
Day 12: Enhanced error handling using centralized exceptions.
"""

import os
import uuid
import logging

from fastapi import APIRouter, File, UploadFile

from backend.schemas.contract_schema import UploadResponse
from backend.services.tracking import create_contract
from backend.utils.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    UnsupportedFileTypeError,
)

logger = logging.getLogger("contract_ai.upload")

router = APIRouter()

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"application/pdf"}
ALLOWED_EXTENSIONS = {".pdf"}


@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload a PDF contract for processing.

    Validates:
      - File extension (.pdf only)
      - MIME content type (application/pdf only)
      - File size (max 20 MB)
      - Non-empty file content

    Returns contract_id for use in subsequent endpoints.
    """
    # --- Validate file extension ---
    _, ext = os.path.splitext(file.filename or "")
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported file type '{ext}'. Only PDF files are accepted."
        )

    # --- Validate MIME type ---
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise UnsupportedFileTypeError(
            f"Unsupported content type '{file.content_type}'. "
            f"Only application/pdf is accepted."
        )

    # --- Read and validate size ---
    contents = await file.read()

    if len(contents) == 0:
        raise EmptyFileError()

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(
            size_mb=len(contents) / (1024 * 1024),
            max_mb=MAX_FILE_SIZE_MB,
        )

    # --- Validate PDF magic bytes ---
    if not contents[:5] == b"%PDF-":
        raise UnsupportedFileTypeError(
            "File does not appear to be a valid PDF "
            "(missing PDF header signature)."
        )

    # --- Save file ---
    contract_id = str(uuid.uuid4())
    safe_filename = f"{contract_id}{ext.lower()}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(contents)

    # --- Track in DB ---
    create_contract(
        contract_id=contract_id,
        filename=file.filename or "unknown.pdf",
        file_size_bytes=len(contents),
    )

    logger.info(
        f"Uploaded contract {contract_id} — "
        f"{file.filename} ({len(contents) / 1024:.1f} KB)"
    )

    return UploadResponse(
        contract_id=contract_id,
        filename=file.filename or "unknown.pdf",
        status="uploaded",
        message="File uploaded successfully",
    )
