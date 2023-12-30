from fastapi import APIRouter

from app.controllers.auth_controller import AuthController
from app.schemas.auth_schema import LoginSchema, RegisterSchema, BearerSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=BearerSchema)
async def login(data: LoginSchema) -> dict[str, str]:
    return await AuthController.login(data)


@router.post("/register", response_model=BearerSchema)
async def register(data: RegisterSchema) -> dict[str, str]:
    return await AuthController.register(data)
