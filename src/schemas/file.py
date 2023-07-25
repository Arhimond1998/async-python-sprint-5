from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    id_user: UUID
    path: str
    size: int


class FileUpdate(FileCreate):
    pass


class FileInDBBase(FileBase):
    id_file: UUID
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool

    class Config:
        orm_mode = True


# Properties to return to client
class File(FileInDBBase):
    pass
