from src.services.repository.repository_db import RepositoryDB
from src.models.user import UserTable
from src.schemas.user import UserCreate, UserUpdate


class RepositoryUser(RepositoryDB[UserTable, UserCreate, UserUpdate]):
    pass


user_rep = RepositoryUser(UserTable)
