from sqlalchemy import Column, DateTime, Integer, String, func, select
from sqlalchemy.dialects.postgresql import insert
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app.core.database import AsyncSession, Base
from app.schemas.auth_schema import RegisterSchema


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    @classmethod
    async def create(cls, data: RegisterSchema, db_session: AsyncSession) -> int:
        user = await cls.get_by_email(db_session=db_session, email=data.email)
        if user:
            return user.id

        obj_in_data = jsonable_encoder(data)
        stmt = (insert(UserModel)
                .values(**obj_in_data)
                .returning(UserModel.id))

        result = await db_session.execute(stmt)
        await db_session.flush()
        return result.scalars().first()

    @staticmethod
    async def get_by_email(email: EmailStr, db_session: AsyncSession) -> "UserModel":
        stmt = select(UserModel) \
                .where(UserModel.email == email)
        result = await db_session.execute(stmt)

        return result.scalars().first()

    @staticmethod
    async def get_by_id(id_: int, db_session: AsyncSession) -> "UserModel":
        stmt = select(UserModel) \
                .where(UserModel.id == id_)
        result = await db_session.execute(stmt)

        return result.scalars().first()

    @classmethod
    async def check_login(
        cls,
        email: EmailStr,
        password: str,
        db_session: AsyncSession
    ) -> "UserModel":
        stmt = (select(UserModel)
                .where(UserModel.email == email,
                       UserModel.password == password))
        result = await db_session.execute(stmt)
        return result.scalars().first()
