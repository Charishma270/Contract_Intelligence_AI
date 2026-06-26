"""
Two-Factor Authentication Routes
==================================
TOTP-based 2FA using pyotp.

Endpoints:
  - POST /api/auth/2fa/setup    → Generate TOTP secret + provisioning URI
  - POST /api/auth/2fa/verify   → Verify a TOTP code and enable 2FA
  - POST /api/auth/2fa/disable  → Disable 2FA for the user
"""

import logging
import io
import base64

import pyotp
import qrcode

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from backend.models.user_model import User
from backend.schemas.auth_schema import MessageResponse
from backend.services.tracking import SessionLocal
from backend.utils.jwt_utils import get_current_user_id
from backend.utils.exceptions import (
    AuthenticationError,
    ContractAIError,
)

logger = logging.getLogger("contract_ai.2fa")

router = APIRouter()


# -----------------------------------------------------------------
# Request schemas
# -----------------------------------------------------------------
class TwoFactorVerifyRequest(BaseModel):
    """Request to verify a TOTP code."""
    code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="6-digit TOTP code from authenticator app.",
    )


# -----------------------------------------------------------------
# Response schemas
# -----------------------------------------------------------------
class TwoFactorSetupResponse(BaseModel):
    """Response with TOTP secret and QR code for setup."""
    success: bool
    message: str
    secret: str
    provisioning_uri: str
    qr_code_base64: str


# -----------------------------------------------------------------
# POST /api/auth/2fa/setup
# -----------------------------------------------------------------
@router.post(
    "/2fa/setup",
    response_model=TwoFactorSetupResponse,
)
async def setup_two_factor(
    user_id: int = Depends(get_current_user_id),
):
    """Generate a TOTP secret and return QR code for authenticator app setup.

    The user must verify the code via /2fa/verify to actually enable 2FA.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise AuthenticationError("User not found.")

        if user.two_factor_enabled:
            raise ContractAIError(
                message="Two-factor authentication is already enabled.",
                status_code=400,
            )

        # Generate new TOTP secret
        secret = pyotp.random_base32()
        user.totp_secret = secret
        db.commit()

        # Create provisioning URI for authenticator apps
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="Contract Intelligence AI",
        )

        # Generate QR code as base64 PNG
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        img = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        logger.info(
            f"2FA setup initiated for user {user_id}"
        )

        return TwoFactorSetupResponse(
            success=True,
            message=(
                "Scan the QR code with your authenticator app, "
                "then verify with a 6-digit code."
            ),
            secret=secret,
            provisioning_uri=provisioning_uri,
            qr_code_base64=f"data:image/png;base64,{qr_base64}",
        )
    finally:
        db.close()


# -----------------------------------------------------------------
# POST /api/auth/2fa/verify
# -----------------------------------------------------------------
@router.post(
    "/2fa/verify",
    response_model=MessageResponse,
)
async def verify_two_factor(
    body: TwoFactorVerifyRequest,
    user_id: int = Depends(get_current_user_id),
):
    """Verify a TOTP code and enable 2FA for the user."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise AuthenticationError("User not found.")

        if not user.totp_secret:
            raise ContractAIError(
                message="2FA setup not initiated. Call /2fa/setup first.",
                status_code=400,
            )

        # Verify the TOTP code
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(body.code, valid_window=1):
            raise ContractAIError(
                message="Invalid 2FA code. Please try again.",
                status_code=400,
            )

        # Enable 2FA
        user.two_factor_enabled = True
        db.commit()

        logger.info(
            f"2FA enabled for user {user_id}"
        )

        return MessageResponse(
            success=True,
            message="Two-factor authentication enabled successfully.",
        )
    finally:
        db.close()


# -----------------------------------------------------------------
# POST /api/auth/2fa/disable
# -----------------------------------------------------------------
@router.post(
    "/2fa/disable",
    response_model=MessageResponse,
)
async def disable_two_factor(
    body: TwoFactorVerifyRequest,
    user_id: int = Depends(get_current_user_id),
):
    """Disable 2FA after verifying current TOTP code."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise AuthenticationError("User not found.")

        if not user.two_factor_enabled:
            raise ContractAIError(
                message="Two-factor authentication is not enabled.",
                status_code=400,
            )

        # Verify the TOTP code before disabling
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(body.code, valid_window=1):
            raise ContractAIError(
                message="Invalid 2FA code. Cannot disable.",
                status_code=400,
            )

        user.two_factor_enabled = False
        user.totp_secret = None
        db.commit()

        logger.info(
            f"2FA disabled for user {user_id}"
        )

        return MessageResponse(
            success=True,
            message="Two-factor authentication disabled.",
        )
    finally:
        db.close()


# -----------------------------------------------------------------
# POST /api/auth/2fa/login — Complete login with 2FA code
# -----------------------------------------------------------------
class TwoFactorLoginRequest(BaseModel):
    """Request to complete login with 2FA code."""
    code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="6-digit TOTP code from authenticator app.",
    )


@router.post(
    "/2fa/login",
    response_model=dict,
)
async def login_with_two_factor(
    body: TwoFactorLoginRequest,
    user_id: int = Depends(get_current_user_id),
):
    """Complete login by verifying the 2FA code.

    Called after POST /api/auth/login returns requires_2fa=True.
    The temporary token from login is used as the Bearer token.
    Returns a full-session JWT on success.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise AuthenticationError("User not found.")

        if not user.two_factor_enabled or not user.totp_secret:
            raise ContractAIError(
                message="2FA is not enabled for this account.",
                status_code=400,
            )

        # Verify the TOTP code
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(body.code, valid_window=1):
            raise ContractAIError(
                message="Invalid 2FA code.",
                status_code=401,
            )

        # Issue full-session token
        from backend.utils.jwt_utils import create_access_token
        token = create_access_token(user.id)

        logger.info(
            f"2FA login completed for user {user_id}"
        )

        return {
            "success": True,
            "message": "2FA verification successful. Login complete.",
            "token": token,
        }
    finally:
        db.close()
