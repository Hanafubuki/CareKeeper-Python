from app.core.exceptions.base import UnauthorizedException, NotFoundException, ForbiddenException


class JWTDecodeError(UnauthorizedException):
    message = "Invalid token (couldn't decode)"


class JWTExpiredError(UnauthorizedException):
    message = "Token expired"


class InvalidBearerToken(ForbiddenException):
    message = "Invalid authentication scheme."


class CredentialError(UnauthorizedException):
    message = "Could not validate credentials"


class UserNotFound(NotFoundException):
    message = "User not found"


class EmailOrPasswordIsWrong(UnauthorizedException):
    message = "Email or password is wrong"
