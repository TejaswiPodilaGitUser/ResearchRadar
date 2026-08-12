import { httpClient } from "./axiosClient";

import type {
  PaperDetail,
  PaperSearchParams,
  PaginatedPaperResponse,
} from "../types/paper";

/**
 * Retrieve paginated research papers.
 */
export async function getPapers(
  params: PaperSearchParams = {},
): Promise<PaginatedPaperResponse> {
  const response =
    await httpClient.get<PaginatedPaperResponse>(
      "/api/papers",
      {
        params,
      },
    );

  return response.data;
}

/**
 * Retrieve a single paper by its identifier.
 */
export async function getPaperById(
  paperId: number,
): Promise<PaperDetail> {
  const response =
    await httpClient.get<PaperDetail>(
      `/api/papers/${paperId}`,
    );

  return response.data;
}

export const paperApi = {
  getPapers,
  getPaperById,
};