from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.services.repository.repository_db import RepositoryDB
from src.models.file import FileTable
from src.schemas.file import FileCreate, FileUpdate
from src.services.utils import redis_cached_async


class RepositoryFile(RepositoryDB[FileTable, FileCreate, FileUpdate]):

    @redis_cached_async(arg_slice=slice(2, 3))
    async def get_file_path(self, db: AsyncSession, id_file: UUID) -> str | None:
        statement = select(self._model).where(FileTable.id_file == id_file)
        result = (await db.execute(statement=statement)).scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='File not found')
        return result.path


file_rep = RepositoryFile(FileTable)
