from sqlalchemy import and_, func, select, update
from structlog import get_logger

from src.db.conn import (
    async_session as async_session,
    async_session_null as async_session_null,
    session_factory,
    session_null_factory,
    dispose_engine
)
from src.db.models import Person


logger = get_logger(__name__)


async def query_person_by_name(name: str):
    async with async_session() as db_session:
        try:
            await dispose_engine()
            query = select(Person).where(Person.name == name)
            logger.info("Executing query", function="query_person_by_name")
            result = await db_session.execute(query)
            logger.info("Executed query", function="query_person_by_name")
            return result.scalars().first()
        except Exception as exc:
            logger.error("Worker error", function="query_person_by_name", exc=exc)
            raise exc
        finally:
            logger.info("Closing DB conn")
            await db_session.close()
            await dispose_engine()


async def persist_person(name: str):
    async with async_session() as db_session:
        try:
            await dispose_engine()
            new_obj = Person(name=name)
            db_session.add(new_obj)
            logger.info("Commiting", function="persist_person")
            await db_session.commit()
            logger.info("Commited", function="persist_person")
        except Exception as exc:
            logger.error("Worker error", function="persist_person", exc=exc)
            raise exc
        finally:
            logger.info("Closing DB conn")
            await db_session.close()
            await dispose_engine()
