from sqlalchemy import Column, String, DateTime, func, UUID

from src.db.db import Base
import uuid


class UserTable(Base):
    __tablename__ = "user"
    __table_args__ = (
        {'schema': 'file_app'}
    )

    id_user = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
