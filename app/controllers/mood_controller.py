from datetime import date

from app.core.database import AsyncSession
from app.core.exceptions.base import NotFoundDataException
from app.models.mood import MoodModel
from app.schemas.mood_schema import MoodSchema


class MoodTrackerController:
    @staticmethod
    async def get(user_id: int, date_: date):
        async with AsyncSession() as db_session:
            mood = await MoodModel.get_by_user_date(user_id=user_id, date_=date_, db_session=db_session)
            if not mood:
                raise NotFoundDataException
        return mood

    @staticmethod
    async def list_all(user_id: int):
        async with AsyncSession() as db_session:
            moods = await MoodModel.list_by_user_id(user_id=user_id, db_session=db_session)
            if not moods:
                raise NotFoundDataException
        return moods

    @staticmethod
    async def create(data: MoodSchema, user_id: int):
        async with AsyncSession() as db_session:
            mood = await MoodModel.create(user_id=user_id, data=data, db_session=db_session)
            await db_session.commit()
        return mood

    @staticmethod
    async def update(date_: date, user_id: int, data: MoodSchema):
        async with AsyncSession() as db_session:
            mood = await MoodModel.update(user_id=user_id, date_=date_, data=data, db_session=db_session)
            await db_session.commit()
        return mood

    @staticmethod
    async def delete(date_: date, user_id: int):
        async with AsyncSession() as db_session:
            await MoodModel.delete(user_id=user_id, date_=date_, db_session=db_session)
            await db_session.commit()
