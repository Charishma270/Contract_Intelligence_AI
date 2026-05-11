from typing import List
from pydantic import BaseModel, Field


class OCRChunk(BaseModel):
    contract_id: str = Field(...)
    chunk_id: str = Field(...)
    page: int = Field(..., ge=1)
    text: str = Field(...)


class OCROutput(BaseModel):
    contract_id: str = Field(...)
    chunks: List[OCRChunk] = Field(default_factory=list)
    total_pages: int = Field(0, ge=0)
