from collections import deque
from threading import Lock


class ApiMetrics:
    """
    In-memory API performance metrics.

    Tracks:
    - Total requests
    - Total errors
    - Response times
    - Average response time
    - P90 latency
    - P95 latency
    - P99 latency

    Note:
    Metrics are stored in memory and are reset when
    the application restarts.
    """

    MAX_SAMPLES = 10_000

    def __init__(self) -> None:
        self._lock = Lock()

        self._request_count = 0
        self._error_count = 0

        self._response_times: deque[float] = deque(
            maxlen=self.MAX_SAMPLES
        )

    # =========================================================
    # Record Request
    # =========================================================

    def record_request(
        self,
        response_time_ms: float,
        is_error: bool,
    ) -> None:
        """
        Record one completed API request.
        """

        with self._lock:
            self._request_count += 1

            self._response_times.append(
                response_time_ms
            )

            if is_error:
                self._error_count += 1

    # =========================================================
    # Percentile Calculation
    # =========================================================

    @staticmethod
    def _percentile(
        values: list[float],
        percentile: float,
    ) -> float:
        """
        Calculate a percentile from response times.

        Example:
            percentile=0.90 -> P90
            percentile=0.95 -> P95
            percentile=0.99 -> P99
        """

        if not values:
            return 0.0

        sorted_values = sorted(values)

        index = int(
            len(sorted_values) * percentile
        )

        index = min(
            index,
            len(sorted_values) - 1,
        )

        return sorted_values[index]

    # =========================================================
    # Get Metrics
    # =========================================================

    def get_metrics(self) -> dict:
        """
        Return current API performance metrics.
        """

        with self._lock:

            request_count = self._request_count

            error_count = self._error_count

            response_times = list(
                self._response_times
            )

        # -----------------------------------------------------
        # Response Time Metrics
        # -----------------------------------------------------

        if response_times:

            average_response_time = (
                sum(response_times)
                / len(response_times)
            )

            p90_latency = self._percentile(
                response_times,
                0.90,
            )

            p95_latency = self._percentile(
                response_times,
                0.95,
            )

            p99_latency = self._percentile(
                response_times,
                0.99,
            )

        else:

            average_response_time = 0.0

            p90_latency = 0.0

            p95_latency = 0.0

            p99_latency = 0.0

        # -----------------------------------------------------
        # Error Rate
        # -----------------------------------------------------

        error_rate = (
            (error_count / request_count) * 100
            if request_count > 0
            else 0.0
        )

        # -----------------------------------------------------
        # Response
        # -----------------------------------------------------

        return {
            "requests": request_count,

            "avg_response_ms": round(
                average_response_time,
                2,
            ),

            "p90_latency_ms": round(
                p90_latency,
                2,
            ),

            "p95_latency_ms": round(
                p95_latency,
                2,
            ),

            "p99_latency_ms": round(
                p99_latency,
                2,
            ),

            "errors": error_count,

            "error_rate": round(
                error_rate,
                2,
            ),
        }


# =============================================================
# Global Metrics Instance
# =============================================================

api_metrics = ApiMetrics()