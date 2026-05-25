from typing import List, Optional
from pydantic import BaseModel, Field


class OCRChunk(BaseModel):
    contract_id: str = Field(...)
    chunk_id: str = Field(...)
    page: int = Field(..., ge=1)
    text: str = Field(...)
    source_file: Optional[str] = Field(
        None, description="Original PDF file path"
    )
    extraction_method: Optional[str] = Field(
        None, description="'pdfplumber' or 'tesseract'"
    )


class OCROutput(BaseModel):
    contract_id: str = Field(...)
    chunks: List[OCRChunk] = Field(default_factory=list)
    total_pages: int = Field(0, ge=0)
    extraction_method: Optional[str] = Field(
        None,
        description="Primary method used: 'pdfplumber' or 'tesseract'",
    )
    processing_time_seconds: Optional[float] = Field(
        None, description="Total OCR processing time in seconds"
    )
