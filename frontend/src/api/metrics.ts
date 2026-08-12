import { httpClient } from "./axiosClient";

export interface MetricsResponse {
  papers: number;
  authors: number;
  topics: number;
  year_range: {
    from: number | null;
    to: number | null;
  };
}

/**
 * Retrieve Research Radar metrics.
 */
export async function getMetrics(): Promise<MetricsResponse> {
  const response = await httpClient.get<MetricsResponse>(
    "/api/metrics",
  );

  return response.data;
}