from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, UUID, ForeignKey
from src.db.db import Base
from src.models.user import UserTable
import uuid


class FileTable(Base):
    __tablename__ = "file"
    __table_args__ = (
        {'schema': 'file_app'}
    )

    id_file = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(ForeignKey(UserTable.id_user), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    path = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)
    is_downloadable = Column(Boolean, default=True)
