import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getSimilarPapers,
} from "../api/recommendationApi";

import type {
  PaperDetail,
} from "../types/paper";

interface UseRecommendationsResult {
  results: PaperDetail[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useRecommendations(
  paperId: number | null,
  limit = 10
): UseRecommendationsResult {
  const [results, setResults] =
    useState<PaperDetail[]>(
      []
    );

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const fetchRecommendations =
    useCallback(async () => {
      if (paperId === null) {
        setResults([]);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response =
          await getSimilarPapers(
            paperId,
            limit
          );

        setResults(response);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Unable to load recommendations.";

        setError(message);
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, [paperId, limit]);

  useEffect(() => {
    void fetchRecommendations();
  }, [fetchRecommendations]);

  return {
    results,
    loading,
    error,
    refetch: fetchRecommendations,
  };
}