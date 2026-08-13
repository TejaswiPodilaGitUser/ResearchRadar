import { httpClient } from "./axiosClient";

import type { PaperListItem } from "../types/paper";

import { SEARCH_CONFIG } from "../config/search";

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
  // GET /api/search
  // ----------------------------------------------------------

  semanticSearch: async ({
    query,
    limit = SEARCH_CONFIG.MAX_SEARCH_RESULTS,
  }: SearchParams): Promise<PaperListItem[]> => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      return [];
    }

    const response = await httpClient.get<PaperListItem[]>(
      SEARCH_CONFIG.SEMANTIC_SEARCH_ENDPOINT,
      {
        params: {
          q: trimmedQuery,
          limit,
        },
      },
    );

    return response.data;
  },

  // ----------------------------------------------------------
  // Hybrid Search
  // GET /api/search/hybrid
  // ----------------------------------------------------------

  hybridSearch: async ({
    query,
    limit = SEARCH_CONFIG.MAX_SEARCH_RESULTS,
  }: SearchParams): Promise<PaperListItem[]> => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      return [];
    }

    const response = await httpClient.get<PaperListItem[]>(
      SEARCH_CONFIG.HYBRID_SEARCH_ENDPOINT,
      {
        params: {
          q: trimmedQuery,
          limit,
        },
      },
    );

    return response.data;
  },
});