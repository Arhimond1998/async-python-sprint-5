import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from jose import jwt, JWTError
from src.schemas.user import UserBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserBase:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Authorization required",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logging.critical(str(e))
        raise credentials_exception

    return UserBase(username=username)


async def user_required(current_user: UserBase = Depends(get_current_user)) -> UserBase:
    return current_user


async def login_required(user: UserBase = Depends(get_current_user)) -> bool:
    return True
