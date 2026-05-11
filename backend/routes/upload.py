import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.contract_schema import UploadResponse
from backend.services.tracking import create_contract

router = APIRouter()

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"application/pdf"}
ALLOWED_EXTENSIONS = {".pdf"}


@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_contract(file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename or "")
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Only PDF files are accepted.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type '{file.content_type}'. Only application/pdf is accepted.",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(contents) / (1024*1024):.1f} MB). "
                   f"Maximum allowed is {MAX_FILE_SIZE_MB} MB.",
        )

    contract_id = str(uuid.uuid4())
    safe_filename = f"{contract_id}{ext.lower()}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(contents)

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
