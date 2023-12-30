import time
import jwt

from app.core.exceptions.security import JWTExpiredError, JWTDecodeError
from app.core.settings import settings


class JWTHandler:
    async def create_token(self, user_id: int):
        payload = {
            "sub": user_id,
            "expires": time.time() + (settings.expire_minutes*60)
        }
        return await self.encode(payload=payload)

    @staticmethod
    async def encode(payload):
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    async def decode(token):
        try:
            decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            if decoded_token["expires"] >= time.time():
                return decoded_token
            else:
                raise JWTExpiredError()
        except:
            raise JWTDecodeError()
