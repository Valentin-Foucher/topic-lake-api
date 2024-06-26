from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from topic_lake_api.domain.interfaces.base import Repository

if TYPE_CHECKING:
    from topic_lake_api.domain.entities import Topic


class ITopicsRepository(Repository, ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> list['Topic']:
        pass

    @abstractmethod
    def create(self, user_id: int, parent_topic_id: Optional[int], content: str):
        pass

    @abstractmethod
    def get(self, topic_id: int) -> 'Topic':
        pass

    @abstractmethod
    def delete(self, user_id: int, topic_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        pass

    @abstractmethod
    def exists(self, parent_topic_id: Optional[int], content: str) -> bool:
        pass
