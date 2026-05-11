import os
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Enum, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from backend.schemas.contract_schema import ContractMetadata, ContractStatus

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "contracts.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ContractRecord(Base):
    __tablename__ = "contracts"

    contract_id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(
        Enum(ContractStatus),
        default=ContractStatus.UPLOADED,
        nullable=False,
    )
    error_message = Column(String, nullable=True)
    file_size_bytes = Column(Integer, nullable=True)


def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_contract(
    contract_id: str,
    filename: str,
    file_size_bytes: Optional[int] = None,
) -> ContractMetadata:
    db = SessionLocal()
    try:
        record = ContractRecord(
            contract_id=contract_id,
            filename=filename,
            upload_time=datetime.utcnow(),
            status=ContractStatus.UPLOADED,
            file_size_bytes=file_size_bytes,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return _to_metadata(record)
    finally:
        db.close()


def get_contract(contract_id: str) -> Optional[ContractMetadata]:
    db = SessionLocal()
    try:
        record = db.query(ContractRecord).filter(
            ContractRecord.contract_id == contract_id
        ).first()
        return _to_metadata(record) if record else None
    finally:
        db.close()


def list_contracts(skip: int = 0, limit: int = 20) -> List[ContractMetadata]:
    db = SessionLocal()
    try:
        records = (
            db.query(ContractRecord)
            .order_by(ContractRecord.upload_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_to_metadata(r) for r in records]
    finally:
        db.close()


def update_status(
    contract_id: str,
    status: ContractStatus,
    error_message: Optional[str] = None,
) -> Optional[ContractMetadata]:
    db = SessionLocal()
    try:
        record = db.query(ContractRecord).filter(
            ContractRecord.contract_id == contract_id
        ).first()
        if not record:
            return None
        record.status = status
        if error_message is not None:
            record.error_message = error_message
        db.commit()
        db.refresh(record)
        return _to_metadata(record)
    finally:
        db.close()


def _to_metadata(record: ContractRecord) -> ContractMetadata:
    return ContractMetadata(
        contract_id=record.contract_id,
        filename=record.filename,
        upload_time=record.upload_time,
        status=record.status,
        error_message=record.error_message,
        file_size_bytes=record.file_size_bytes,
    )
