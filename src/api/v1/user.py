import logging

from jose import jwt

from fastapi import Depends, APIRouter
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.schemas.user import UserCreate, User, UserAuth
from src.services.repository.repository_user import user_rep
from src.db.session import get_session
from src.models.user import UserTable


router = APIRouter(prefix='/user')


@router.post('/register', response_model=User, status_code=HTTP_201_CREATED)
async def register_user(
        data: UserCreate,
        db: AsyncSession = Depends(get_session),
):
    logging.info('Register new user %s', data.username)
    user_db = await user_rep.get(db, UserTable.username == data.username)
    if user_db:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail='User already exists')
    res = await user_rep.create(db, obj_in=data)
    return res


@router.post('/auth', status_code=HTTP_201_CREATED)
async def auth_user(
        data: UserAuth,
        db: AsyncSession = Depends(get_session),
) -> str:
    logging.info('User auth %s', data.username)
    user_db = await user_rep.get(db, (UserTable.username == data.username) & (UserTable.password == data.password))
    if not user_db:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Wrong username/password')

    token = jwt.encode(
        {
            'username': user_db.username,
            'password': user_db.password,
            'id': str(user_db.id_user)
        },
        settings.JWT_SECRET,
        settings.JWT_ALGORITHM
    )
    return token
