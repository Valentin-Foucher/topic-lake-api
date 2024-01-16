from typing import Optional

from sqlalchemy import select, null, literal
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Topic as TopicModel
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository


class TopicsRepository(ITopicsRepository):

    @staticmethod
    def _get_topics_as_treeview(*filters: list[bool], limit: int = 1):
        anchor_member = session.query(TopicModel, literal(0).label('level')) \
            .filter(*filters) \
            .order_by(TopicModel.id) \
            .limit(limit) \
            .cte(name='ancestors_id', recursive=True)

        parent = aliased(anchor_member, name='p')
        children = aliased(TopicModel, name='c')

        recursive_member = anchor_member.union_all(
            session
            .query(children, (parent.c.level + 1).label('level'))
            .filter(children.parent_topic_id == parent.c.id)
            .order_by(parent.c.id)
        )

        return session.scalars(
            select(TopicModel, recursive_member.c.level)
            .where(
                TopicModel.id == recursive_member.c.id,
                recursive_member.c.level == 0
            )
        )

    def list(self, limit: int = 100) -> list[Topic]:
        topic_list = self._get_topics_as_treeview(TopicModel.parent_topic == null(), limit=limit)
        return [topic.as_dataclass() for topic in topic_list]

    def create(self, user_id: int, parent_topic_id: Optional[int], content: str) -> int:
        t = TopicModel(user_id=user_id, parent_topic_id=parent_topic_id, content=content)
        session.add(t)
        session.flush()
        session.commit()
        return t.id

    def get(self, topic_id: int) -> Optional[Topic]:
        try:
            topic = self._get_topics_as_treeview(TopicModel.id == topic_id) \
                .one()
        except NoResultFound:
            return None

        return topic.as_dataclass()

    def delete(self, topic_id: int) -> bool:
        deleted_rows = session.execute(
            TopicModel.__table__.delete()
            .where()
            .returning(TopicModel.id)
        ).fetchall()
        return len(deleted_rows) != 0
