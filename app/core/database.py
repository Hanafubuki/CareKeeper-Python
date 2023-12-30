from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.settings import settings

Base = declarative_base()  # transforms basic classes into sqlalchemy classes

engine = create_async_engine(settings.db_uri)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

"""
    Usage
    from app.database import AsyncSession
    async with AsyncSession() as db:
        user = User.get_by_id(user_id=12345, db=db)
"""


async def get_db():
    db = AsyncSession()

    try:
        yield db
    finally:
        await db.close()
