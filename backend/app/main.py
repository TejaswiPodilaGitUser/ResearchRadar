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