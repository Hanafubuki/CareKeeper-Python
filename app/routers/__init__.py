from fastapi import APIRouter, Depends

from app.routers.auth_router import router as auth_router
from app.routers.mood_router import router as mood_tracker_router
from app.dependencies.token_verifier import VerifyToken


def get_main_router() -> APIRouter:
    router = APIRouter(prefix="/v1")

    routers_without_auth = APIRouter()
    routers_without_auth.include_router(auth_router)

    routers_with_auth = APIRouter(dependencies=[Depends(VerifyToken())])
    routers_with_auth.include_router(mood_tracker_router)

    router.include_router(routers_without_auth)
    router.include_router(routers_with_auth)

    return router
