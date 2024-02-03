from sqlalchemy import and_, func, select, update
from sqlalchemy.orm import selectinload

from src.db.conn import (
    async_session as async_session,
    dispose_engine

)
from src.db.models import Person


async def query_or_persist(name: str):
    print("CHEGOU")
    async with async_session() as db_session:
        try:
            query = select(Person).where(Person.name == name)
            result = await db_session.execute(query)
            obj = result.scalars().first()
            if not obj:
                new_obj = Person(name=name)
                db_session.add(new_obj)
                await db_session.commit()
            return obj
        except Exception as exc:
            print(" worker error ")
            print(exc)
        finally:
            print("CLOSED")
            await db_session.close()
            await dispose_engine()

