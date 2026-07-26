from models.user import User
from repositories.user_repo import UserRepository
from schemas.auth import UserRegister, UserLogin, Token
from core.security import get_password_hash, verify_password, create_access_token
from exceptions.custom import InvalidCredentialsException, BaseHealthcareException
from utils.otp import otp_manager
from utils.email import send_email
from core.logger import logger

class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    async def register_user(self, user_in: UserRegister) -> User:
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise BaseHealthcareException("An account with this email address already exists.")
        
        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            phone_number=user_in.phone_number
        )
        return await self.user_repo.create(new_user)

    async def login_user(self, credentials: UserLogin) -> Token:
        user = await self.user_repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise InvalidCredentialsException()
        
        access_token = create_access_token(subject=user.id)
        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user.role
        )

    async def send_otp(self, email: str) -> bool:
        otp = otp_manager.generate_otp(email)
        subject = "Your HealthCare App Verification Code"
        html_content = (
            f"<h3>Healthcare Security Verification</h3>"
            f"<p>Your OTP verification code is: <strong>{otp}</strong></p>"
            f"<p>This code is valid for 5 minutes. If you did not request this, please ignore this email.</p>"
        )
        try:
            await send_email(email, subject, html_content)
            return True
        except Exception as e:
            logger.error(f"Failed to dispatch OTP email: {str(e)}")
            return False

    async def verify_otp(self, email: str, otp: str) -> bool:
        return otp_manager.verify_otp(email, otp)
