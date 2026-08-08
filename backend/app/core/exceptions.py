from typing import Any

from app.core.error_codes import ErrorCode


class AppException(Exception):
    """
    Base application exception.

    All expected application errors should derive
    from this exception.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: ErrorCode,
        details: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details

        super().__init__(message)


class BadRequestException(AppException):

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.BAD_REQUEST,
        details: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code=error_code,
            details=details,
        )


class ResourceNotFoundException(AppException):

    def __init__(
        self,
        resource: str,
        resource_id: Any,
    ):
        super().__init__(
            message=(
                f"{resource} with id "
                f"{resource_id} not found"
            ),
            status_code=404,
            error_code=(
                ErrorCode.RESOURCE_NOT_FOUND
            ),
        )


class DuplicateResourceException(AppException):

    def __init__(
        self,
        message: str = "Resource already exists",
        details: Any = None,
    ):
        super().__init__(
            message=message,
            status_code=409,
            error_code=(
                ErrorCode.DUPLICATE_RESOURCE
            ),
            details=details,
        )


class DatabaseException(AppException):

    def __init__(
        self,
        message: str = "Database operation failed",
        error_code: ErrorCode = (
            ErrorCode.DATABASE_ERROR
        ),
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
        )


class EmbeddingException(AppException):

    def __init__(
        self,
        message: str = "Embedding generation failed",
        error_code: ErrorCode = (
            ErrorCode.EMBEDDING_ERROR
        ),
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
        )


class SearchException(AppException):

    def __init__(
        self,
        message: str = "Search operation failed",
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=ErrorCode.SEARCH_ERROR,
        )


class RecommendationException(AppException):

    def __init__(
        self,
        message: str = "Recommendation operation failed",
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=ErrorCode.RECOMMENDATION_ERROR,
        )


class RateLimitException(AppException):

    def __init__(
        self,
        message: str = "Rate limit exceeded",
    ):
        super().__init__(
            message=message,
            status_code=429,
            error_code=(
                ErrorCode.RATE_LIMIT_EXCEEDED
            ),
        )

