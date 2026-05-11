"""
Upload Route — /api/upload
==========================
Accepts PDF uploads, validates file type & size,
generates a contract_id, persists the file, and
creates a tracking record in the database.
"""

import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.contract_schema import UploadResponse
from backend.services.tracking import create_contract

router = APIRouter()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"application/pdf"}
ALLOWED_EXTENSIONS = {".pdf"}


# ---------------------------------------------------------------------------
# POST /api/upload
# ---------------------------------------------------------------------------
@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload a legal contract PDF for analysis.

    - Validates MIME type and file extension
    - Rejects files larger than 20 MB
    - Generates a unique contract_id (UUID4)
    - Saves to the uploads/ directory
    - Creates a tracking record in the database
    """

    # --- Validate file extension ---
    _, ext = os.path.splitext(file.filename or "")
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Only PDF files are accepted.",
        )

    # --- Validate content type ---
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type '{file.content_type}'. Only application/pdf is accepted.",
        )

    # --- Read file and check size ---
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(contents) / (1024*1024):.1f} MB). "
                   f"Maximum allowed is {MAX_FILE_SIZE_MB} MB.",
        )

    # --- Generate contract ID and save ---
    contract_id = str(uuid.uuid4())
    safe_filename = f"{contract_id}{ext.lower()}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(contents)

    # --- Create tracking record ---
    create_contract(
        contract_id=contract_id,
        filename=file.filename or "unknown.pdf",
        file_size_bytes=len(contents),
    )

    return UploadResponse(
        contract_id=contract_id,
        filename=file.filename or "unknown.pdf",
        status="uploaded",
        message="File uploaded successfully",
    )
