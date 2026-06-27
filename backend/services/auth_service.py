# """
# Auth Service
# =============
# Business logic for user registration, authentication,
# profile updates, and password management.

# Uses passlib/bcrypt for password hashing and the shared
# SQLAlchemy SessionLocal from tracking.py.
# """

# import logging
# from datetime import datetime
# from typing import Optional

# from passlib.context import CryptContext

# from backend.models.user_model import User
# from backend.services.tracking import SessionLocal
# from backend.utils.exceptions import (
#     AuthenticationError,
#     EmailAlreadyExistsError,
#     InvalidCredentialsError,
#     WeakPasswordError,
# )

# logger = logging.getLogger("contract_ai.auth")

# # Password hashing context
# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto",
# )


# # -----------------------------------------------------------------
# # User CRUD
# # -----------------------------------------------------------------
# def get_user_by_id(user_id: int) -> Optional[User]:
#     """Fetch a user by primary key."""
#     db = SessionLocal()
#     try:
#         return db.query(User).filter(
#             User.id == user_id
#         ).first()
#     finally:
#         db.close()


# def get_user_by_email(email: str) -> Optional[User]:
#     """Fetch a user by email (case-insensitive)."""
#     db = SessionLocal()
#     try:
#         return db.query(User).filter(
#             User.email == email.lower()
#         ).first()
#     finally:
#         db.close()


# # -----------------------------------------------------------------
# # Registration
# # -----------------------------------------------------------------
# def create_user(
#     name: str,
#     email: str,
#     password: str,
# ) -> User:
#     """Register a new user.

#     Raises:
#         EmailAlreadyExistsError: If email is already taken.
#         WeakPasswordError: If password is too short.
#     """
#     if len(password) < 6:
#         raise WeakPasswordError(
#             "Password must be at least 6 characters."
#         )

#     email_lower = email.lower()

#     if get_user_by_email(email_lower):
#         raise EmailAlreadyExistsError(email_lower)

#     hashed = pwd_context.hash(password)

#     db = SessionLocal()
#     try:
#         user = User(
#             name=name,
#             email=email_lower,
#             hashed_password=hashed,
#             role="User",
#             created_at=datetime.utcnow(),
#             last_login=datetime.utcnow(),
#         )
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#         logger.info(
#             f"User registered: id={user.id}, "
#             f"email={user.email}"
#         )
#         return user
#     finally:
#         db.close()


# # -----------------------------------------------------------------
# # Authentication
# # -----------------------------------------------------------------
# def authenticate_user(
#     email: str,
#     password: str,
# ) -> User:
#     """Verify credentials and update last_login.

#     Raises:
#         InvalidCredentialsError: If email/password don't match.
#     """
#     user = get_user_by_email(email)

#     if not user:
#         raise InvalidCredentialsError()

#     if not pwd_context.verify(password, user.hashed_password):
#         raise InvalidCredentialsError()

#     # Update last_login
#     db = SessionLocal()
#     try:
#         db_user = db.query(User).filter(
#             User.id == user.id
#         ).first()
#         if db_user:
#             db_user.last_login = datetime.utcnow()
#             db.commit()
#             db.refresh(db_user)
#             logger.info(
#                 f"User logged in: id={db_user.id}, "
#                 f"email={db_user.email}"
#             )
#             return db_user
#         return user
#     finally:
#         db.close()


# # -----------------------------------------------------------------
# # Profile management
# # -----------------------------------------------------------------
# def update_user_profile(
#     user_id: int,
#     name: Optional[str] = None,
#     email: Optional[str] = None,
#     phone: Optional[str] = None,
#     organization: Optional[str] = None,
# ) -> User:
#     """Update a user's profile fields.

#     Raises:
#         AuthenticationError: If user not found.
#         EmailAlreadyExistsError: If new email is taken.
#     """
#     db = SessionLocal()
#     try:
#         user = db.query(User).filter(
#             User.id == user_id
#         ).first()

#         if not user:
#             raise AuthenticationError(
#                 "User not found."
#             )

#         # Check email uniqueness if changing
#         if email and email.lower() != user.email:
#             existing = db.query(User).filter(
#                 User.email == email.lower()
#             ).first()
#             if existing:
#                 raise EmailAlreadyExistsError(
#                     email.lower()
#                 )
#             user.email = email.lower()

#         if name is not None:
#             user.name = name
#         if phone is not None:
#             user.phone = phone
#         if organization is not None:
#             user.organization = organization

#         db.commit()
#         db.refresh(user)

#         logger.info(
#             f"Profile updated: id={user.id}"
#         )
#         return user
#     finally:
#         db.close()


# def change_user_password(
#     user_id: int,
#     current_password: str,
#     new_password: str,
#     confirm_password: str,
# ) -> None:
#     """Change a user's password after verifying the current one.

#     Raises:
#         AuthenticationError: If user not found.
#         InvalidCredentialsError: If current password is wrong.
#         WeakPasswordError: If new password fails validation.
#     """
#     if new_password != confirm_password:
#         raise WeakPasswordError(
#             "New password and confirm password do not match."
#         )

#     if len(new_password) < 6:
#         raise WeakPasswordError(
#             "Password must be at least 6 characters."
#         )

#     db = SessionLocal()
#     try:
#         user = db.query(User).filter(
#             User.id == user_id
#         ).first()

#         if not user:
#             raise AuthenticationError(
#                 "User not found."
#             )

#         if not pwd_context.verify(
#             current_password, user.hashed_password
#         ):
#             raise InvalidCredentialsError(
#                 "Current password is incorrect."
#             )

#         user.hashed_password = pwd_context.hash(
#             new_password
#         )
#         db.commit()

#         logger.info(
#             f"Password changed: id={user.id}"
#         )
#     finally:
#         db.close()

"""
Auth Service
=============
Business logic for user registration, authentication,
profile updates, password management, and password reset.
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional, cast

from passlib.context import CryptContext

from backend.models.user_model import User
from backend.services.tracking import SessionLocal
from backend.utils.exceptions import (
    AuthenticationError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    WeakPasswordError,
)

logger = logging.getLogger("contract_ai.auth")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

_password_reset_tokens = {}


def _as_user(user) -> User:
    return cast(User, user)


def get_user_by_id(user_id: int) -> Optional[User]:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return _as_user(user) if user else None
    finally:
        db.close()


def get_user_by_email(email: str) -> Optional[User]:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email.lower()).first()
        return _as_user(user) if user else None
    finally:
        db.close()


def create_user(name: str, email: str, password: str) -> User:
    if len(password) < 6:
        raise WeakPasswordError("Password must be at least 6 characters.")

    email_lower = email.lower()

    if get_user_by_email(email_lower):
        raise EmailAlreadyExistsError(email_lower)

    hashed = pwd_context.hash(password)

    db = SessionLocal()
    try:
        user = User(
            name=name,
            email=email_lower,
            hashed_password=hashed,
            role="User",
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow(),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return _as_user(user)
    finally:
        db.close()


def authenticate_user(email: str, password: str) -> User:
    user = get_user_by_email(email)

    if not user:
        raise InvalidCredentialsError()

    if not pwd_context.verify(password, user.hashed_password):
        raise InvalidCredentialsError()

    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.id == user.id).first()

        if db_user:
            db_user = _as_user(db_user)
            db_user.last_login = datetime.utcnow()
            db.commit()
            db.refresh(db_user)
            return db_user

        return user
    finally:
        db.close()


def update_user_profile(
    user_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    organization: Optional[str] = None,
) -> User:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise AuthenticationError("User not found.")

        user = _as_user(user)

        if email and email.lower() != user.email:
            existing = db.query(User).filter(User.email == email.lower()).first()

            if existing:
                raise EmailAlreadyExistsError(email.lower())

            user.email = email.lower()

        if name is not None:
            user.name = name

        if phone is not None:
            user.phone = phone

        if organization is not None:
            user.organization = organization

        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()


def change_user_password(
    user_id: int,
    current_password: str,
    new_password: str,
    confirm_password: str,
) -> None:
    if new_password != confirm_password:
        raise WeakPasswordError(
            "New password and confirm password do not match."
        )

    if len(new_password) < 6:
        raise WeakPasswordError("Password must be at least 6 characters.")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise AuthenticationError("User not found.")

        user = _as_user(user)

        if not pwd_context.verify(current_password, user.hashed_password):
            raise InvalidCredentialsError("Current password is incorrect.")

        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
    finally:
        db.close()


def create_password_reset_token(email: str) -> str:
    user = get_user_by_email(email)

    if not user:
        raise AuthenticationError("Email address not found.")

    token = secrets.token_urlsafe(32)

    _password_reset_tokens[token] = {
        "user_id": user.id,
        "expires_at": datetime.utcnow() + timedelta(minutes=30),
    }

    logger.info(f"Password reset token created for user_id={user.id}")

    return token


def reset_user_password(
    token: str,
    new_password: str,
    confirm_password: str,
) -> None:
    if new_password != confirm_password:
        raise WeakPasswordError(
            "New password and confirm password do not match."
        )

    if len(new_password) < 6:
        raise WeakPasswordError("Password must be at least 6 characters.")

    token_data = _password_reset_tokens.get(token)

    if not token_data:
        raise AuthenticationError("Invalid or expired reset token.")

    if datetime.utcnow() > token_data["expires_at"]:
        _password_reset_tokens.pop(token, None)
        raise AuthenticationError("Reset token has expired.")

    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.id == token_data["user_id"]
        ).first()

        if not user:
            raise AuthenticationError("User not found.")

        user = _as_user(user)

        user.hashed_password = pwd_context.hash(new_password)
        db.commit()

        _password_reset_tokens.pop(token, None)

        logger.info(f"Password reset completed for user_id={user.id}")
    finally:
        db.close()