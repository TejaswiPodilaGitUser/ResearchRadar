import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { paperApi } from "../api/paperApi";

import type {
  PaginatedPaperResponse,
  PaperSearchParams,
} from "../types/paper";

interface UsePapersResult {
  data: PaginatedPaperResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function usePapers(
  params: PaperSearchParams
): UsePapersResult {
  const [data, setData] =
    useState<PaginatedPaperResponse | null>(
      null
    );

  const [loading, setLoading] =
    useState<boolean>(false);

  const [error, setError] =
    useState<string | null>(null);

  const fetchPapers = useCallback(
    async () => {
      setLoading(true);
      setError(null);

      try {
        const result =
          await paperApi.getPapers(params);

        setData(result);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Unable to load papers.";

        setError(message);
      } finally {
        setLoading(false);
      }
    },
    [
      params.page,
      params.size,
      params.keyword,
      params.year,
      params.topic,
      params.author,
    ]
  );

  useEffect(() => {
    // Only fetch if there's a search query or filter applied
    const hasSearch =
      params.keyword ||
      params.year ||
      params.topic ||
      params.author;

    if (hasSearch) {
      void fetchPapers();
    }
  }, [fetchPapers]);

  return {
    data,
    loading,
    error,
    refetch: fetchPapers,
  };
}