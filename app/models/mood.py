from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, Date, String
from sqlalchemy import func, select, update, delete
from sqlalchemy.dialects.postgresql import insert
from fastapi.encoders import jsonable_encoder
from datetime import date as date_datetime, datetime

from app.core.database import AsyncSession, Base
from app.core.exceptions.base import DuplicateValueException, NotFoundDataException
from app.schemas.mood_schema import MoodSchema


class MoodModel(Base):
    __tablename__ = "moods"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    mood = Column(String(255), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    @staticmethod
    async def list_by_user_id(user_id: int, db_session: AsyncSession) -> list["MoodModel"]:
        stmt = select(MoodModel) \
            .where(MoodModel.user_id == user_id)
        result = await db_session.execute(stmt)

        return result.scalars().all()

    @staticmethod
    async def get_by_user_date(user_id: int, date_: date_datetime, db_session: AsyncSession) -> "MoodModel":
        stmt = select(MoodModel) \
                .where(MoodModel.user_id == user_id,
                       MoodModel.date == date_)
        result = await db_session.execute(stmt)

        return result.scalars().first()

    @classmethod
    async def create(cls, data: MoodSchema, user_id: int, db_session: AsyncSession) -> int:
        mood = await cls.get_by_user_date(db_session=db_session, date_=data.date, user_id=user_id)
        if mood:
            raise DuplicateValueException

        obj_in_data = jsonable_encoder(data)
        obj_in_data["user_id"] = user_id
        obj_in_data["date"] = datetime.strptime(obj_in_data["date"],"%Y-%m-%d")
        stmt = (insert(MoodModel)
                .values(**obj_in_data)
                .returning(MoodModel.id))

        result = await db_session.execute(stmt)
        await db_session.flush()
        return result.scalars().first()

    @classmethod
    async def update(cls, data: MoodSchema, user_id: int, date_: date_datetime, db_session: AsyncSession) -> "MoodModel":
        mood = await cls.get_by_user_date(db_session=db_session, date_=date_, user_id=user_id)
        if not mood:
            raise NotFoundDataException

        obj_in_data = jsonable_encoder(data)
        stmt = (update(MoodModel)
                .where(MoodModel.user_id == user_id,
                       MoodModel.date == date_)
                .values(**obj_in_data))

        await db_session.execute(stmt)
        await db_session.flush()
        return mood

    @classmethod
    async def delete(cls, user_id: int, date_: date_datetime, db_session: AsyncSession):
        mood = await cls.get_by_user_date(db_session=db_session, date_=date_, user_id=user_id)
        if not mood:
            raise NotFoundDataException

        stmt = (delete(MoodModel)
                .where(MoodModel.user_id == user_id,
                       MoodModel.date == date_))

        await db_session.execute(stmt)
