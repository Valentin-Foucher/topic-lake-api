from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository, IUsersRepository
from topic_lake_api.use_cases.topics.delete import DeleteTopic


class DeleteTopicController(Controller):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, topic_id: int):
        DeleteTopic(self._topics_repository, self._users_repository).execute(
            user_id,
            topic_id
        )
