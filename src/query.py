from sqlalchemy import select

from src.db.conn import async_session
from src.db import models


async def execute() -> None:
    async with async_session() as db_session:
        try:
            query = select(models.Person)
            result = await db_session.execute(query)
            results = result.scalars().all()
            print(sorted([x.name for x in results]))
        finally:
            await db_session.close()
