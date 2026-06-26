"""
Auth & Profile Schemas
=======================
Pydantic models for authentication and profile management
request/response validation.

Response shapes are designed to match the frontend AuthContext
contract (id, name, email, role, organization, phone, joinedDate, lastLogin).
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# -----------------------------------------------------------------
# Auth — Requests
# -----------------------------------------------------------------
class SignupRequest(BaseModel):
    """POST /api/auth/signup request body."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the user.",
    )
    email: EmailStr = Field(
        ...,
        description="Email address (must be unique).",
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Password (min 6 characters).",
    )


class LoginRequest(BaseModel):
    """POST /api/auth/login request body."""

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
    )
    password: str = Field(
        ...,
        description="Account password.",
    )


# -----------------------------------------------------------------
# Shared — User response shape
# -----------------------------------------------------------------
class UserResponse(BaseModel):
    """User data returned to the frontend.

    Fields match what the frontend AuthContext stores as `currentUser`.
    """

    id: int
    name: str
    email: str
    role: str
    organization: Optional[str] = None
    phone: Optional[str] = None
    joinedDate: Optional[str] = None
    lastLogin: Optional[str] = None
    twoFactorEnabled: bool = False

    model_config = {"from_attributes": True}


# -----------------------------------------------------------------
# Auth — Responses
# -----------------------------------------------------------------
class AuthResponse(BaseModel):
    """Response for signup and login endpoints."""

    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[UserResponse] = None
    requires_2fa: bool = False


class MessageResponse(BaseModel):
    """Generic success/error message response."""

    success: bool
    message: str


# -----------------------------------------------------------------
# Profile — Requests
# -----------------------------------------------------------------
class ProfileUpdateRequest(BaseModel):
    """PUT /api/profile request body."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
    )
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        None,
        max_length=20,
    )
    organization: Optional[str] = Field(
        None,
        max_length=100,
    )


class ChangePasswordRequest(BaseModel):
    """PUT /api/profile/change-password request body."""

    currentPassword: str = Field(
        ...,
        description="Current password for verification.",
    )
    newPassword: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="New password (min 6 characters).",
    )
    confirmPassword: str = Field(
        ...,
        description="Must match newPassword.",
    )
