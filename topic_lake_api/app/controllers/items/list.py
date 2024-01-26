from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.items import ListItemsPresenter
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.items.list_items import ListItems


class ListItemsController(Controller):
    def __init__(self, presenter: ListItemsPresenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    async def execute(self, topic_id: int):
        result = await ListItems(self._repository).execute(topic_id)
        return self._presenter.present(result)

