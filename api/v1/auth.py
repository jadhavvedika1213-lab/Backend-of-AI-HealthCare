from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import UserRegister, UserLogin, Token, OTPRequest, OTPVerify
from services.auth_service import AuthService
from core.database import get_db
from utils.response import APIResponse

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db = Depends(get_db)):
    service = AuthService(db)
    user = await service.register_user(user_in)
    return APIResponse.success(
        message="User registered successfully. Welcome email scheduled.",
        data={"id": user.id, "email": user.email, "full_name": user.full_name},
        status_code=status.HTTP_201_CREATED
    )

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db = Depends(get_db)):
    service = AuthService(db)
    token = await service.login_user(credentials)
    return token

@router.post("/oauth/token", response_model=Token)
async def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    """
    OAuth2 standard compatibility endpoint (used by Swagger Docs).
    """
    service = AuthService(db)
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return await service.login_user(credentials)

@router.post("/otp/request")
async def request_otp(payload: OTPRequest, db = Depends(get_db)):
    service = AuthService(db)
    success = await service.send_otp(payload.email)
    if success:
        return APIResponse.success(message="OTP code sent successfully to your email.")
    return APIResponse.error(message="Failed to dispatch OTP. Please try again.")

@router.post("/otp/verify")
async def verify_otp(payload: OTPVerify, db = Depends(get_db)):
    service = AuthService(db)
    is_valid = await service.verify_otp(payload.email, payload.otp)
    if is_valid:
        return APIResponse.success(message="OTP verification successful.")
    return APIResponse.error(message="Invalid or expired OTP code.")
