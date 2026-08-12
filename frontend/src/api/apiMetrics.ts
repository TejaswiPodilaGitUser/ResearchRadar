import { httpClient } from "./axiosClient";


/**
 * API performance metrics.
 */
export interface ApiMetricsResponse {
  requests: number;
  avg_response_ms: number;
  errors: number;
  error_rate: number;
  p90_latency_ms: number;
  p95_latency_ms: number;
  p99_latency_ms: number;
}


/**
 * Retrieve API performance metrics.
 */
export async function getApiMetrics(): Promise<ApiMetricsResponse> {
  const response =
    await httpClient.get<ApiMetricsResponse>(
      "/api/metrics/performance",
    );

  return response.data;
}