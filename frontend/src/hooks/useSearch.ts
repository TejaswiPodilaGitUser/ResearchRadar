import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { searchApi } from "../api/searchApi";

import type {
  PaperListItem,
} from "../types/paper";

interface UseSearchResult {
  results: PaperListItem[];
  loading: boolean;
  error: string | null;
}

export function useSearch(
  query: string,
  limit = 10
): UseSearchResult {
  const [results, setResults] =
    useState<PaperListItem[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const executeSearch = useCallback(
    async () => {
      const normalizedQuery =
        query.trim();

      if (!normalizedQuery) {
        setResults([]);
        setError(null);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response =
          await searchApi.hybridSearch({
            query: normalizedQuery,
            limit,
          });

        setResults(response);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Search failed.";

        setError(message);
        setResults([]);
      } finally {
        setLoading(false);
      }
    },
    [query, limit]
  );

  useEffect(() => {
    void executeSearch();
  }, [executeSearch]);

  return {
    results,
    loading,
    error,
  };
}