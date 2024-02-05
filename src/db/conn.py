from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import settings


engine = create_async_engine(settings.DB_URI, **settings.DB_ENGINE_OPTIONS)
async_session = async_sessionmaker(bind=engine, **{
    'expire_on_commit': False,
    'autocommit': False,
    'autoflush': False,
})


engine_null = create_async_engine(
    settings.DB_URI, **settings.DB_ENGINE_OPTIONS_NULL
)
async_session_null = async_sessionmaker(bind=engine_null, **{
    'expire_on_commit': False,
    'autocommit': False,
    'autoflush': False,
})


async def dispose_engine() -> None:
    await engine.dispose(close=False)


async def session_factory():
    engine = create_async_engine(settings.DB_URI, **settings.DB_ENGINE_OPTIONS)
    async_session_factory = async_sessionmaker(bind=engine, **{
        'expire_on_commit': False,
        'autocommit': False,
        'autoflush': False,
    })
    async with async_session_factory() as session:
        yield session


async def session_null_factory():
    engine_null = create_async_engine(
        settings.DB_URI, **settings.DB_ENGINE_OPTIONS_NULL
    )
    async_session_factory = async_sessionmaker(bind=engine_null, **{
        'expire_on_commit': False,
        'autocommit': False,
        'autoflush': False,
    })
    async with async_session_factory() as session:
        yield session

