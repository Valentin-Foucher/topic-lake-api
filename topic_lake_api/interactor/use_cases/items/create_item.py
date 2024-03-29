from topic_lake_api.interactor.exceptions import DoesNotExist, InvalidInputData
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase
from topic_lake_api.interactor.utils.item_utils import determine_rank


class CreateItem(UseCase):
    def __init__(self, items_repository: IItemsRepository, topics_repository: ITopicsRepository,
                 users_repository: IUsersRepository):
        self._items_repository = items_repository
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, topic_id: int, user_id: int, content: str, rank: int):
        if not self._users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        if not self._topics_repository.get(topic_id):
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        if self._items_repository.exists(topic_id, content):
            raise InvalidInputData('This item already exists')

        self._items_repository.update_ranks_for_topic(topic_id, rank)
        return self._items_repository.create(
            topic_id,
            user_id,
            content,
            determine_rank(self._items_repository, rank, topic_id)
        )
