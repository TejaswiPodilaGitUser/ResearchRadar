import { httpClient } from "./axiosClient";

import type {
  PaperListItem,
} from "../types/paper";

// ============================================================
// Search Types
// ============================================================

export interface SearchParams {
  query: string;
  limit?: number;
}

// ============================================================
// Search API
// ============================================================

export const searchApi = Object.freeze({
  // ----------------------------------------------------------
  // Semantic Search
  // ----------------------------------------------------------

  semanticSearch: async ({
    query,
    limit = 10,
  }: SearchParams): Promise<
    PaperListItem[]
  > => {
    const response = await httpClient.get<
      PaperListItem[]
    >(
      "/search",
      {
        params: {
          q: query,
          limit,
        },
      }
    );
    return response.data;
  },

  // ----------------------------------------------------------
  // Hybrid Search
  // ----------------------------------------------------------

  hybridSearch: async ({
    query,
    limit = 10,
  }: SearchParams): Promise<
    PaperListItem[]
  > => {
    const response = await httpClient.get<
      PaperListItem[]
    >(
      "/search/hybrid",
      {
        params: {
          q: query,
          limit,
        },
      }
    );
    return response.data;
  },
});