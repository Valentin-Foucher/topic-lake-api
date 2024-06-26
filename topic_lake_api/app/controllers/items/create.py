from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.domain.interfaces.base import Presenter
from topic_lake_api.domain.interfaces.repositories import IItemsRepository, ITopicsRepository, IUsersRepository
from topic_lake_api.use_cases.items.create import CreateItem


class CreateItemController(Controller):
    def __init__(self, presenter: Presenter, items_repository: IItemsRepository, topics_repository: ITopicsRepository,
                 users_repository: IUsersRepository):
        self._presenter = presenter
        self._items_repository = items_repository
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, topic_id: int, user_id: int, content: str, rank: int):
        result = CreateItem(self._items_repository, self._topics_repository, self._users_repository) \
            .execute(topic_id, user_id, content, rank)
        return self._presenter.present(result)

