"""
User Model
===========
SQLAlchemy ORM model for the `users` table.

Stores user credentials (bcrypt-hashed), profile metadata,
and security flags used by the auth & profile APIs.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)

from backend.services.tracking import Base


class User(Base):
    """Registered user account."""

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name = Column(
        String,
        nullable=False,
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password = Column(
        String,
        nullable=False,
    )
    role = Column(
        String,
        default="User",
    )
    organization = Column(
        String,
        nullable=True,
    )
    phone = Column(
        String,
        nullable=True,
    )
    two_factor_enabled = Column(
        Boolean,
        default=False,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
    last_login = Column(
        DateTime,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"email={self.email!r}, "
            f"name={self.name!r})"
        )
