# """
# Auth Routes
# ============
# Authentication endpoints: signup, login, logout, and current user.

# All responses match the shape expected by the frontend AuthContext.
# """

# import logging

# from fastapi import APIRouter, Depends

# from backend.schemas.auth_schema import (
#     AuthResponse,
#     ChangePasswordRequest,
#     LoginRequest,
#     MessageResponse,
#     SignupRequest,
#     UserResponse,
# )
# from backend.services.auth_service import (
#     authenticate_user,
#     create_user,
#     get_user_by_id,
# )
# from backend.utils.jwt_utils import (
#     create_access_token,
#     get_current_user_id,
# )

# logger = logging.getLogger("contract_ai.auth")

# router = APIRouter()


# # -----------------------------------------------------------------
# # Helpers
# # -----------------------------------------------------------------
# def _user_to_response(user) -> UserResponse:
#     """Convert a User ORM object to the frontend-friendly shape."""
#     joined = (
#         user.created_at.strftime("%B %Y")
#         if user.created_at
#         else None
#     )
#     last = (
#         "Today"
#         if user.last_login
#         else None
#     )
#     return UserResponse(
#         id=user.id,
#         name=user.name,
#         email=user.email,
#         role=user.role or "User",
#         organization=user.organization,
#         phone=user.phone,
#         joinedDate=joined,
#         lastLogin=last,
#         twoFactorEnabled=user.two_factor_enabled or False,
#     )


# # -----------------------------------------------------------------
# # POST /api/auth/signup
# # -----------------------------------------------------------------
# @router.post(
#     "/signup",
#     response_model=AuthResponse,
# )
# async def signup(body: SignupRequest):
#     """Register a new user and return a JWT token."""

#     user = create_user(
#         name=body.name,
#         email=body.email,
#         password=body.password,
#     )

#     token = create_access_token(user.id)
#     user_data = _user_to_response(user)

#     logger.info(
#         f"Signup successful: {user.email}"
#     )

#     return AuthResponse(
#         success=True,
#         message="Signup successful.",
#         token=token,
#         user=user_data,
#     )


# # -----------------------------------------------------------------
# # POST /api/auth/login
# # -----------------------------------------------------------------
# @router.post(
#     "/login",
#     response_model=AuthResponse,
# )
# async def login(body: LoginRequest):
#     """Authenticate a user and return a JWT token.

#     If 2FA is enabled, returns requires_2fa=True and a
#     temporary token. The client must then verify the TOTP
#     code via POST /api/auth/2fa/login.
#     """

#     user = authenticate_user(
#         email=body.email,
#         password=body.password,
#     )

#     # If 2FA is enabled, don't issue full token yet
#     if user.two_factor_enabled:
#         # Issue a short-lived token for 2FA verification
#         from datetime import timedelta
#         temp_token = create_access_token(
#             user.id,
#             expires_delta=timedelta(minutes=5),
#         )
#         return AuthResponse(
#             success=True,
#             message="2FA verification required.",
#             token=temp_token,
#             user=_user_to_response(user),
#             requires_2fa=True,
#         )

#     token = create_access_token(user.id)
#     user_data = _user_to_response(user)

#     return AuthResponse(
#         success=True,
#         message="Login successful.",
#         token=token,
#         user=user_data,
#     )


# # -----------------------------------------------------------------
# # POST /api/auth/logout
# # -----------------------------------------------------------------
# @router.post(
#     "/logout",
#     response_model=MessageResponse,
# )
# async def logout():
#     """Logout endpoint.

#     JWT is stateless — the client simply discards the token.
#     This endpoint exists for API completeness and frontend parity.
#     """
#     return MessageResponse(
#         success=True,
#         message="Logged out successfully.",
#     )


# # -----------------------------------------------------------------
# # GET /api/auth/me
# # -----------------------------------------------------------------
# @router.get(
#     "/me",
#     response_model=AuthResponse,
# )
# async def me(
#     user_id: int = Depends(get_current_user_id),
# ):
#     """Return the currently authenticated user's data."""

#     user = get_user_by_id(user_id)

#     if not user:
#         return AuthResponse(
#             success=False,
#             message="User not found.",
#         )

#     user_data = _user_to_response(user)

#     return AuthResponse(
#         success=True,
#         message="Authenticated.",
#         user=user_data,
#     )




"""
Auth Routes
============
Authentication endpoints: signup, login, logout, current user,
forgot password, and reset password.
"""

import logging
from datetime import timedelta

from fastapi import APIRouter, Depends

from backend.schemas.auth_schema import (
    AuthResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    MessageResponse,
    ResetPasswordRequest,
    SignupRequest,
    UserResponse,
)
from backend.services.auth_service import (
    authenticate_user,
    create_password_reset_token,
    create_user,
    get_user_by_id,
    reset_user_password,
)
from backend.utils.jwt_utils import (
    create_access_token,
    get_current_user_id,
)

logger = logging.getLogger("contract_ai.auth")

router = APIRouter()


def _user_to_response(user) -> UserResponse:
    joined = user.created_at.strftime("%B %Y") if user.created_at else None
    last = "Today" if user.last_login else None

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


@router.post("/signup", response_model=AuthResponse)
async def signup(body: SignupRequest):
    user = create_user(
        name=body.name,
        email=body.email,
        password=body.password,
    )

    token = create_access_token(user.id)

    return AuthResponse(
        success=True,
        message="Signup successful.",
        token=token,
        user=_user_to_response(user),
    )


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest):
    user = authenticate_user(
        email=body.email,
        password=body.password,
    )

    if user.two_factor_enabled:
        temp_token = create_access_token(
            user.id,
            expires_delta=timedelta(minutes=5),
        )

        return AuthResponse(
            success=True,
            message="2FA verification required.",
            token=temp_token,
            user=_user_to_response(user),
            requires_2fa=True,
        )

    token = create_access_token(user.id)

    return AuthResponse(
        success=True,
        message="Login successful.",
        token=token,
        user=_user_to_response(user),
    )


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(body: ForgotPasswordRequest):
    token = create_password_reset_token(body.email)

    return ForgotPasswordResponse(
        success=True,
        message=(
            "Password reset token generated. "
            "Use this token to reset your password."
        ),
        reset_token=token,
    )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(body: ResetPasswordRequest):
    reset_user_password(
        token=body.token,
        new_password=body.newPassword,
        confirm_password=body.confirmPassword,
    )

    return MessageResponse(
        success=True,
        message="Password reset successful. You can now login.",
    )


@router.post("/logout", response_model=MessageResponse)
async def logout():
    return MessageResponse(
        success=True,
        message="Logged out successfully.",
    )


@router.get("/me", response_model=AuthResponse)
async def me(user_id: int = Depends(get_current_user_id)):
    user = get_user_by_id(user_id)

    if not user:
        return AuthResponse(
            success=False,
            message="User not found.",
        )

    return AuthResponse(
        success=True,
        message="Authenticated.",
        user=_user_to_response(user),
    )