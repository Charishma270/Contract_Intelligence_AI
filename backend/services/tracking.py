"""
Contract Tracking Service
=========================
SQLAlchemy + SQLite for tracking contract status through the pipeline.
Database stored at data/contracts.db.

Day 13: Added structured logging for DB operations.
"""

import os
import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Enum, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from backend.schemas.contract_schema import ContractMetadata, ContractStatus

logger = logging.getLogger("contract_ai.tracking")

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------
DB_PATH = os.path.join("data", "contracts.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------------------------------------------------------------
# ORM Model
# ---------------------------------------------------------------------------
class ContractRecord(Base):
    __tablename__ = "contracts"

    contract_id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default=ContractStatus.UPLOADED.value)
    error_message = Column(String, nullable=True)
    file_size_bytes = Column(Integer, nullable=True)


# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------
def init_db():
    """Create all tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Get a database session (call .close() when done)."""
    db = SessionLocal()
    return db


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------
def create_contract(
    contract_id: str,
    filename: str,
    file_size_bytes: Optional[int] = None,
) -> ContractMetadata:
    """Insert a new contract record after upload."""
    db = get_db()
    try:
        record = ContractRecord(
            contract_id=contract_id,
            filename=filename,
            upload_time=datetime.utcnow(),
            status=ContractStatus.UPLOADED.value,
            file_size_bytes=file_size_bytes,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info(
            f"Contract created: id={contract_id}, "
            f"file={filename}, size={file_size_bytes} bytes"
        )
        return _record_to_schema(record)
    finally:
        db.close()


def get_contract(contract_id: str) -> Optional[ContractMetadata]:
    """Fetch a single contract by ID."""
    db = get_db()
    try:
        record = db.query(ContractRecord).filter(
            ContractRecord.contract_id == contract_id
        ).first()
        return _record_to_schema(record) if record else None
    finally:
        db.close()


def list_contracts(skip: int = 0, limit: int = 20) -> List[ContractMetadata]:
    """List contracts with pagination (newest first)."""
    db = get_db()
    try:
        records = (
            db.query(ContractRecord)
            .order_by(ContractRecord.upload_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_record_to_schema(r) for r in records]
    finally:
        db.close()


def update_contract_status(
    contract_id: str,
    status: ContractStatus,
    error_message: Optional[str] = None,
) -> Optional[ContractMetadata]:
    """Update the processing status of a contract."""
    db = get_db()
    try:
        record = db.query(ContractRecord).filter(
            ContractRecord.contract_id == contract_id
        ).first()
        if not record:
            return None
        record.status = status.value
        if error_message is not None:
            record.error_message = error_message
        db.commit()
        db.refresh(record)
        logger.info(
            f"Contract status updated: id={contract_id}, "
            f"status={status.value}"
        )
        return _record_to_schema(record)
    finally:
        db.close()


def get_contract_file_path(contract_id: str) -> Optional[str]:
    """Return the file path for a given contract_id, or None."""
    db = get_db()
    try:
        record = db.query(ContractRecord).filter(
            ContractRecord.contract_id == contract_id
        ).first()
        if not record:
            return None
        ext = os.path.splitext(record.filename)[1] or ".pdf"
        return os.path.join("uploads", f"{contract_id}{ext}")
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------
def _record_to_schema(record: ContractRecord) -> ContractMetadata:
    return ContractMetadata(
        contract_id=record.contract_id,
        filename=record.filename,
        upload_time=record.upload_time,
        status=ContractStatus(record.status),
        error_message=record.error_message,
        file_size_bytes=record.file_size_bytes,
    )
