"""
Profile Routes
===============
Endpoints for viewing and updating the authenticated user's profile
and changing their password.
"""

import logging

from fastapi import APIRouter, Depends

from backend.schemas.auth_schema import (
    AuthResponse,
    ChangePasswordRequest,
    MessageResponse,
    ProfileUpdateRequest,
    UserResponse,
)
from backend.services.auth_service import (
    change_user_password,
    get_user_by_id,
    update_user_profile,
)
from backend.utils.jwt_utils import (
    get_current_user_id,
)

logger = logging.getLogger("contract_ai.profile")

router = APIRouter()


def _user_to_response(user) -> UserResponse:
    """Convert a User ORM object to the frontend-friendly shape."""
    joined = (
        user.created_at.strftime("%B %Y")
        if user.created_at
        else None
    )
    last = (
        "Today"
        if user.last_login
        else None
    )
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role or "User",
        organization=user.organization,
        phone=user.phone,
        joinedDate=joined,
        lastLogin=last,
        twoFactorEnabled=user.two_factor_enabled or False,
    )


# -----------------------------------------------------------------
# GET /api/profile
# -----------------------------------------------------------------
@router.get(
    "/",
    response_model=AuthResponse,
)
async def get_profile(
    user_id: int = Depends(get_current_user_id),
):
    """Get the current user's profile."""

    user = get_user_by_id(user_id)

    if not user:
        return AuthResponse(
            success=False,
            message="User not found.",
        )

    return AuthResponse(
        success=True,
        message="Profile retrieved.",
        user=_user_to_response(user),
    )


# -----------------------------------------------------------------
# PUT /api/profile
# -----------------------------------------------------------------
@router.put(
    "/",
    response_model=AuthResponse,
)
async def update_profile(
    body: ProfileUpdateRequest,
    user_id: int = Depends(get_current_user_id),
):
    """Update the current user's profile."""

    user = update_user_profile(
        user_id=user_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        organization=body.organization,
    )

    logger.info(
        f"Profile updated for user {user_id}"
    )

    return AuthResponse(
        success=True,
        message="Profile updated successfully.",
        user=_user_to_response(user),
    )


# -----------------------------------------------------------------
# PUT /api/profile/change-password
# -----------------------------------------------------------------
@router.put(
    "/change-password",
    response_model=MessageResponse,
)
async def change_password(
    body: ChangePasswordRequest,
    user_id: int = Depends(get_current_user_id),
):
    """Change the current user's password."""

    change_user_password(
        user_id=user_id,
        current_password=body.currentPassword,
        new_password=body.newPassword,
        confirm_password=body.confirmPassword,
    )

    logger.info(
        f"Password changed for user {user_id}"
    )

    return MessageResponse(
        success=True,
        message="Password updated successfully.",
    )
