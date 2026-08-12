import time
import uuid
import logging

from fastapi import Request

from app.core.api_metrics import api_metrics


logger = logging.getLogger(__name__)


async def request_context_middleware(
    request: Request,
    call_next,
):
    """
    Adds request ID, records request duration,
    and captures API performance metrics.
    """

    request_id = request.headers.get(
        "X-Request-ID"
    )

    if not request_id:
        request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        # HTTP 4xx and 5xx responses count as errors.
        is_error = response.status_code >= 400

        api_metrics.record_request(
            response_time_ms=duration_ms,
            is_error=is_error,
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        logger.info(
            "HTTP request completed "
            "method=%s path=%s status=%s "
            "duration_ms=%.2f request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )

        return response

    except Exception:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        # Unhandled exceptions count as errors.
        api_metrics.record_request(
            response_time_ms=duration_ms,
            is_error=True,
        )

        logger.exception(
            "HTTP request failed "
            "method=%s path=%s "
            "duration_ms=%.2f request_id=%s",
            request.method,
            request.url.path,
            duration_ms,
            request_id,
        )

        raise