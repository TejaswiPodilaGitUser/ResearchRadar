from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =====================================================
    # Application
    # =====================================================

    APP_NAME: str = "Research Radar"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = False

    # =====================================================
    # Database
    # =====================================================

    DATABASE_URL: str = Field(
        ...,
        validation_alias="DATABASE_URL",
    )

    # =====================================================
    # OpenAlex
    # =====================================================

    OPENALEX_BASE_URL: str = Field(
        default="https://api.openalex.org",
        validation_alias="OPENALEX_BASE_URL",
    )

    # =====================================================
    # Pagination
    # =====================================================

    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # =====================================================
    # Search
    # =====================================================

    DEFAULT_SEARCH_LIMIT: int = 10
    MAX_SEARCH_RESULTS: int = 100

    MIN_SEARCH_QUERY_LENGTH: int = 2
    MAX_SEARCH_QUERY_LENGTH: int = 500

    # =====================================================
    # Validation
    # =====================================================

    MAX_KEYWORD_LENGTH: int = 500
    MAX_TOPIC_LENGTH: int = 200
    MAX_AUTHOR_LENGTH: int = 200

    MIN_PUBLICATION_YEAR: int = 1900
    MAX_PUBLICATION_YEAR: int = 2100

    # =====================================================
    # Recommendations
    # =====================================================

    RECOMMENDATION_DEFAULT_LIMIT: int = 10
    RECOMMENDATION_MAX_LIMIT: int = 50

    # =====================================================
    # Embeddings
    # =====================================================

    EMBEDDING_MODEL_NAME: str = Field(
        default="all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL_NAME",
    )

    EMBEDDING_DIMENSION: int = Field(
        default=384,
        ge=1,
        validation_alias="EMBEDDING_DIMENSION",
    )

    # =====================================================
    # API / Security Guardrails
    # =====================================================

    MAX_REQUEST_BODY_SIZE_MB: int = 10

    # =====================================================
    # Pydantic Settings
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# =========================================================
# Settings Singleton
# =========================================================

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()