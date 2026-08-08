from enum import StrEnum


class ErrorCode(StrEnum):
    """
    Application-wide error codes.

    These codes are part of the public API contract.
    Do not change existing values once clients depend on them.
    """

    # ========================================================
    # Request / Validation
    # ========================================================

    VALIDATION_ERROR = "VALIDATION_ERROR"
    BAD_REQUEST = "BAD_REQUEST"

    INVALID_PAGINATION = "INVALID_PAGINATION"
    INVALID_PAPER_ID = "INVALID_PAPER_ID"
    INVALID_AUTHOR_ID = "INVALID_AUTHOR_ID"
    INVALID_TOPIC_ID = "INVALID_TOPIC_ID"

    SEARCH_QUERY_EMPTY = "SEARCH_QUERY_EMPTY"
    SEARCH_QUERY_TOO_LONG = "SEARCH_QUERY_TOO_LONG"

    # ========================================================
    # Resources
    # ========================================================

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    DUPLICATE_RESOURCE = "DUPLICATE_RESOURCE"

    # ========================================================
    # Search / AI
    # ========================================================

    SEARCH_ERROR = "SEARCH_ERROR"
    RECOMMENDATION_ERROR = "RECOMMENDATION_ERROR"

    EMBEDDING_ERROR = "EMBEDDING_ERROR"
    EMBEDDING_DIMENSION_MISMATCH = (
        "EMBEDDING_DIMENSION_MISMATCH"
    )

    # ========================================================
    # Ingestion
    # ========================================================

    INGESTION_ERROR = "INGESTION_ERROR"

    OPENALEX_ERROR = "OPENALEX_ERROR"
    OPENALEX_TIMEOUT = "OPENALEX_TIMEOUT"
    OPENALEX_RATE_LIMITED = "OPENALEX_RATE_LIMITED"

    # ========================================================
    # Infrastructure
    # ========================================================

    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_CONNECTION_ERROR = (
        "DATABASE_CONNECTION_ERROR"
    )

    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"

    # ========================================================
    # Security / Traffic
    # ========================================================

    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

    # ========================================================
    # Unexpected
    # ========================================================

    INTERNAL_ERROR = "INTERNAL_ERROR"

