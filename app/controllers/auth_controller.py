from app.core.database import AsyncSession
from app.core.exceptions.security import EmailOrPasswordIsWrong
from app.core.security.jwt import JWTHandler

from app.models import UserModel
from app.schemas.auth_schema import LoginSchema, RegisterSchema


class AuthController:
    @staticmethod
    async def register(data: RegisterSchema) -> dict[str, str]:
        async with AsyncSession() as db_session:
            user_id = await UserModel.create(data=data, db_session=db_session)
            await db_session.commit()
        token = await JWTHandler().create_token(user_id=user_id)
        return {"bearer": token}

    @staticmethod
    async def login(data: LoginSchema) -> dict[str, str]:
        async with AsyncSession() as db_session:
            user = await UserModel.check_login(
                db_session=db_session,
                email=data.email,
                password=data.password
            )

        if not user:
            raise EmailOrPasswordIsWrong()

        token = await JWTHandler().create_token(user_id=user.id)
        return {"bearer": token}
