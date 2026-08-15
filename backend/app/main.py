from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.exceptions import AppException

from app.core.middleware import (
    request_context_middleware,
)

from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)

from app.api.papers import router as papers_router
from app.api.search import router as search_router
from app.api.authors import router as authors_router
from app.api.topics import router as topics_router

from app.api.recommendations import (
    router as recommendations_router,
)

from app.api.metrics import (
    router as metrics_router,
)

from fastapi.openapi.utils import get_openapi


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# ============================================================
# CORS Middleware
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Middleware
# ============================================================

app.middleware("http")(
    request_context_middleware
)


# ============================================================
# Exception Handlers
# ============================================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


# ============================================================
# API Routers
# ============================================================

app.include_router(
    papers_router,
    prefix="/api",
)

app.include_router(
    search_router,
    prefix="/api",
)

app.include_router(
    authors_router,
    prefix="/api",
)

app.include_router(
    topics_router,
    prefix="/api",
)

app.include_router(
    recommendations_router,
    prefix="/api",
)

app.include_router(
    metrics_router,
    prefix="/api",
)


# ============================================================
# Health Check
# ============================================================

@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    """
    Application health check.
    """

    return {
        "status": "UP"
    }


# ============================================================
# Custom OpenAPI
# ============================================================
# This changes ONLY the Swagger/OpenAPI display order.
#
# Actual FastAPI route matching remains safe:
#
# /papers/name
# /papers/collection/ids
# /papers/collection/names
# /papers/{paper_id}
#
# Therefore /papers/name will NOT produce a 422 error.
# ============================================================

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    desired_paper_order = [
        "/api/papers",
        "/api/papers/{paper_id}",
        "/api/papers/name",
        "/api/papers/collection/ids",
        "/api/papers/collection/names",
    ]

    paths = openapi_schema.get("paths", {})

    ordered_paths = {}

    # --------------------------------------------------------
    # Add Papers paths in desired Swagger order
    # --------------------------------------------------------

    for path in desired_paper_order:
        if path in paths:
            ordered_paths[path] = paths[path]

    # --------------------------------------------------------
    # Add all remaining API paths
    # --------------------------------------------------------

    for path, value in paths.items():
        if path not in ordered_paths:
            ordered_paths[path] = value

    openapi_schema["paths"] = ordered_paths

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi