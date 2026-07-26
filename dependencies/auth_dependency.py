from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings
from core.database import get_db
from models.user import User
from repositories.user_repo import UserRepository
from exceptions.custom import InvalidCredentialsException, UserNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise InvalidCredentialsException("Could not validate credentials: missing subject")
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise InvalidCredentialsException("Could not validate credentials: invalid token signature")

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise UserNotFoundException("User not found")
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user
