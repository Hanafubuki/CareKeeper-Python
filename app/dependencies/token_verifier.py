from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security.jwt import JWTHandler
from app.core.exceptions.security import CredentialError, UserNotFound, InvalidBearerToken
from app.models.user import UserModel
from app.core.database import AsyncSession


class VerifyToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(VerifyToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(VerifyToken, self).__call__(request)
        if (credentials and not credentials.scheme == "Bearer") or not credentials:
            raise InvalidBearerToken
        request.state.user = await self.verify_jwt(credentials.credentials)

    @staticmethod
    async def verify_jwt(authorization: str): # = Header(..., alias="Authorization")
        payload = await JWTHandler.decode(authorization)

        user_id: int = payload.get("sub")

        if user_id is None:
            raise CredentialError

        async with AsyncSession() as db_session:
            user = await UserModel.get_by_id(id_=user_id, db_session=db_session)

        if user is None:
            raise UserNotFound
        return user
