import contextlib
import inspect
import logging
import re
from functools import lru_cache
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Session
from sqlalchemy_utils import database_exists, create_database

from topic_lake_api import config
from topic_lake_api.domain.utils.object_utils import get_object_by_name

engine = create_engine(config.get('postgres.connection_string'))

Model = declarative_base(name='Model')


def as_dataclass(model: Model | list[Model]):
    if isinstance(model, list):
        return [as_dataclass(sub) for sub in model]

    clz = get_object_by_name(f'topic_lake_api.domain.entities.{model.__class__.__name__}')
    dataclass_attributes = inspect.signature(clz).parameters
    kwargs = {}

    for c in model.__table__.columns:
        if c.name in dataclass_attributes:
            kwargs[c.name] = getattr(model, c.name)

    for m in model.__mapper__.relationships:
        sub_model_value = getattr(model, m.key)
        if not sub_model_value:
            continue

        # storing nesting object attribute as nested dataclass
        if any(p == m.key and sub_model_value for p in dataclass_attributes):
            kwargs[m.key] = as_dataclass(sub_model_value)

        # storing nesting object attribute as simple parent attribute
        else:
            prefix = f'{m.key}_'
            for complete_name in dataclass_attributes:
                if complete_name.startswith(prefix) and complete_name in dataclass_attributes:
                    kwargs[complete_name] = getattr(sub_model_value, re.sub(prefix, '', complete_name))

    return clz(**kwargs)


Model.as_dataclass = as_dataclass

logger = logging.getLogger(__name__)


@lru_cache
def session_maker() -> sessionmaker:
    return sessionmaker(bind=engine)


@contextlib.contextmanager
def get_session() -> Iterator[Session]:
    s = scoped_session(session_maker())
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def init_db():
    logger.info('Initializing database')
    if not database_exists(engine.url):
        create_database(engine.url)
        Model.metadata.create_all(engine)
    else:
        engine.connect()


def shutdown_db():
    logger.info('Shutting down database connection')
    engine.dispose()
