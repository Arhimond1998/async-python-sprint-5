import logging
from pathlib import Path

from fastapi import Depends, APIRouter, UploadFile
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from starlette.responses import FileResponse
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.file import FileCreate, File
from src.schemas.user import UserBase
from src.services.repository.repository_file import file_rep
from src.db.session import get_session
from src.core.deps.user import get_current_user
from src.models.file import FileTable
from src.core.config import settings
import uuid


router = APIRouter(prefix='/file')


@router.post('/upload', response_model=File, status_code=HTTP_201_CREATED)
async def upload_file(
        path: str,
        file: UploadFile,
        db: AsyncSession = Depends(get_session),
        user: UserBase = Depends(get_current_user),
):
    logging.info('Uploading file by user %s, path %s', user.username, path)
    content = await file.read()
    p = Path('.')
    path = path.strip('/')
    path = f'{settings.UPLOAD_FOLDER}/{path}'

    is_file = '.' in path.split('/')[-1]
    name = file.filename
    if is_file:
        name = path.split('/')[-1]
        p = p / path[: path.rfind('/')]
    else:
        p = p / path
        path = f'{path}/{name}'

    p.mkdir(parents=True, exist_ok=True)

    with open(path, 'wb') as f:
        f.write(content)

    obj_in = FileCreate(
        name=name,
        size=file.size,
        path=path
    )

    res = await file_rep.create(db, obj_in=obj_in)
    return res


@router.get('/download/{path_or_id_file:path}')
async def download_file(
    path_or_id_file: str,
    db: AsyncSession = Depends(get_session),
):
    logging.info('Accessing to file by path %s', path_or_id_file)
    file_not_found_exc = HTTPException(status_code=HTTP_404_NOT_FOUND, detail='File not found')

    # check if we got path to file
    p = Path('.') / settings.UPLOAD_FOLDER / path_or_id_file
    if p.exists():
        return FileResponse(str(p))

    # otherwise we got id
    id_file = path_or_id_file
    logging.info('Accessing to file by id %s', id_file)
    try:
        file_uuid = uuid.UUID(id_file)
    except ValueError:
        raise file_not_found_exc

    file_path = await file_rep.get_file_path(db, file_uuid)

    return FileResponse(file_path)


@router.get('/', response_model=list[File])
async def get_files(
        db: AsyncSession = Depends(get_session),
        user: UserBase = Depends(get_current_user),
):
    logging.info('Retrieve file info for user %s', user)
    return await file_rep.get_multi(db)
