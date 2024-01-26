from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class GetTopic(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    async def execute(self, topic_id: int):
        result = await self._repository.get(topic_id)
        if not result:
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        return result
