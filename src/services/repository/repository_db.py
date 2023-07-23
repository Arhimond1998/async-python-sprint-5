from typing import Any, Generic, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi.encoders import jsonable_encoder


from src.db.db import Base
from src.services.repository.repository_base import Repository


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, *args: Any) -> ModelType | None:
        statement = select(self._model).where(*args)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *args, skip=0, limit=100
    ) -> list[ModelType]:
        statement = select(self._model).where(*args).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType, autocommit: bool = True) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        if autocommit:
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            obj_in: UpdateSchemaType | dict[str, Any],
            *args,
            autocommit: bool = True,
    ):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        query = update(self._model).where(*args).values(**update_data)
        await db.execute(query)
        if autocommit:
            await db.commit()

    async def delete(self, db: AsyncSession, *args, autocommit: bool = True):
        await db.execute(delete(self._model).where(*args))
        if autocommit:
            await db.commit()
