from passlib.context import CryptContext


class PasswordHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    # Should be hashed in the FE
    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)
