from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_lake_api.domain.entities.users import User
from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.infra.repositories.base import SQLRepository


class UsersRepository(SQLRepository, IUsersRepository):
    def create(self, name: str, hashed_password: str) -> int:
        u = UserModel(name=name, password=hashed_password)

        self._session.add(u)
        self._session.flush()

        return u.id

    def get(self, user_id: int) -> Optional[User]:
        try:
            user = self._session.scalars(
                select(UserModel)
                .where(UserModel.id == user_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return user.as_dataclass()

    def get_by_name(self, name: str) -> Optional[User]:
        try:
            user = self._session.scalars(
                select(UserModel)
                .where(UserModel.name == name)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return user.as_dataclass()
