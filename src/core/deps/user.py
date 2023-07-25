import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from jose import jwt, JWTError
from src.schemas.user import UserAuth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserAuth:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Authorization required",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("username")
        id_user: str = payload.get("id")
        if username is None or id_user is None:
            raise credentials_exception
    except JWTError as e:
        logging.critical(str(e))
        raise credentials_exception

    return UserAuth(username=username, id_user=id_user)


async def user_required(current_user: UserAuth = Depends(get_current_user)) -> UserAuth:
    return current_user


async def login_required(user: UserAuth = Depends(get_current_user)) -> bool:
    return True
