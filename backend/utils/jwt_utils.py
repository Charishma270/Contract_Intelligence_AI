"""
JWT Utilities
==============
Token creation, decoding, and a FastAPI dependency
for extracting the current user from the Authorization header.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, Request

from backend.config import settings
from backend.utils.exceptions import (
    AuthenticationError,
)

logger = logging.getLogger("contract_ai.auth")


# -----------------------------------------------------------------
# Token helpers
# -----------------------------------------------------------------
def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token for `user_id`."""

    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        or timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token


def decode_access_token(token: str) -> int:
    """Decode a JWT and return the user_id (``sub`` claim).

    Raises:
        AuthenticationError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = int(payload["sub"])
        return user_id

    except jwt.ExpiredSignatureError:
        raise AuthenticationError(
            "Token has expired. Please log in again."
        )
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise AuthenticationError(
            "Invalid authentication token."
        )


# -----------------------------------------------------------------
# FastAPI dependency
# -----------------------------------------------------------------
def get_current_user_id(
    request: Request,
) -> int:
    """FastAPI dependency — extract user_id from Bearer token.

    Usage::

        @router.get("/protected")
        async def protected(
            user_id: int = Depends(get_current_user_id),
        ):
            ...
    """
    auth_header: Optional[str] = request.headers.get(
        "Authorization"
    )

    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationError(
            "Missing or invalid Authorization header. "
            "Expected: Bearer <token>"
        )

    token = auth_header[7:]  # strip "Bearer "
    return decode_access_token(token)
