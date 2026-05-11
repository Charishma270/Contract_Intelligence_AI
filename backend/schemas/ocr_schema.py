"""
OCR Schemas
===========
Pydantic models for OCR pipeline input/output.
Matches the output format expected from Sruthi's OCR extraction module.
"""

from typing import List
from pydantic import BaseModel, Field


class OCRChunk(BaseModel):
    """A single chunk of OCR-extracted text from a contract page."""
    contract_id: str = Field(..., description="UUID of the parent contract")
    chunk_id: str = Field(..., description="Unique identifier for this chunk")
    page: int = Field(..., ge=1, description="1-indexed page number")
    text: str = Field(..., description="Extracted text content")


class OCROutput(BaseModel):
    """Complete OCR output for one contract document."""
    contract_id: str = Field(..., description="UUID of the contract")
    chunks: List[OCRChunk] = Field(default_factory=list, description="Ordered list of text chunks")
    total_pages: int = Field(0, ge=0, description="Total pages processed")
