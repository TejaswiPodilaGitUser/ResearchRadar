import logging

from fastapi import (
    Request,
    status,
)

from fastapi.exceptions import (
    RequestValidationError,
)

from fastapi.responses import JSONResponse

from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppException


logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    """
    Handle known application exceptions.
    """

    logger.warning(
        "Application error: "
        "method=%s path=%s code=%s message=%s",
        request.method,
        request.url.path,
        exc.error_code,
        exc.message,
    )

    response = {
        "error": {
            "code": exc.error_code,
            "message": exc.message,
        }
    }

    if exc.details is not None:
        response["error"]["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle FastAPI/Pydantic validation errors.
    """

    logger.warning(
        "Validation error: method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    """
    Handle unexpected database errors.

    Do not expose database internals to clients.
    """

    logger.exception(
        "Database error: method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred",
            }
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Final safety net for unexpected exceptions.
    """

    logger.exception(
        "Unhandled exception: method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )

