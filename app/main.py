import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import get_main_router
from app.core.exceptions.base import CustomException

logger = logging.getLogger(__name__)


def setup_error_handlers(app_: FastAPI):
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        status_code, message = 500, str(exc)
        if isinstance(exc, CustomException):
            status_code = int(exc.code)
            message = exc.message

        return JSONResponse(
            status_code=status_code,
            content={"message": message},
        )


def get_app() -> FastAPI:
    logger.info("Starting app...")
    app_ = FastAPI()

    # Bind routes
    logger.info("Configuring routers for app...")
    app_.include_router(get_main_router())
    setup_error_handlers(app_)

    return app_


app = get_app()
