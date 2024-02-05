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


async def query_or_persist(name: str, value: int):
    # async for db_session in session_factory():
    async with async_session() as db_session:
        try:
            await dispose_engine()

            logger.info("Querying person", function="query_or_persist", value=value)
            query = select(Person).where(Person.name == name)
            logger.info("Executing query", function="query_or_persist", value=value)
            result = await db_session.execute(query)
            logger.info("Executed query", function="query_or_persist", value=value)
            obj = result.scalars().first()
            if not obj:
                new_obj = Person(name=name)
                db_session.add(new_obj)
                logger.info("Commiting", function="query_or_persist", value=value)
                await db_session.commit()
                logger.info("Commited", function="query_or_persist", value=value)
            return obj
        except Exception as exc:
            logger.error("Worker error", function="query_or_persist", value=value, exc=exc, )
            raise exc
        finally:
            logger.info("Closing DB conn", value=value)
            await db_session.close()
            await dispose_engine()

