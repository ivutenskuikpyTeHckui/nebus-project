from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.exceptions import LogicException
from app.utilities.logger import logger


class LogicExceptionHandler:
    @staticmethod
    async def handler(request: Request, exc: LogicException) -> JSONResponse:
        logger.error(str(exc), extra={"extra": exc.extra, "path": request.url.path})
        return JSONResponse(
            content={"message": str(exc), "result": "error"},
            status_code=exc.status_code,
        )


class RequestValidationErrorHandler:
    @staticmethod
    async def handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.error(str(exc), extra={"path": request.url.path})
        return JSONResponse(
            content={
                "message": "Validation error",
                "result": "error",
                "detail": jsonable_encoder(exc.errors()),
            },
            status_code=422,
        )


class ExceptionHandler:
    @staticmethod
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(str(exc), extra={"path": request.url.path})
        return JSONResponse(
            content={"message": "Something went wrong!", "result": "error"},
            status_code=500,
        )
