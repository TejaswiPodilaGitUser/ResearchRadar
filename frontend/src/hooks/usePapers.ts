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

// ============================================================
// Types
// ============================================================

interface UsePapersResult {
  data: PaginatedPaperResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

// ============================================================
// Hook
// ============================================================

export function usePapers(
  params: PaperSearchParams,
  enabled = true,
): UsePapersResult {
  const [data, setData] =
    useState<PaginatedPaperResponse | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  // ==========================================================
  // Fetch papers
  // ==========================================================

  const fetchPapers =
    useCallback(async (): Promise<void> => {

      // --------------------------------------------------------
      // IMPORTANT:
      // Do not call API when search is disabled.
      // --------------------------------------------------------

      if (!enabled) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const result =
          await paperApi.getPapers(params);

        setData(result);

      } catch (err) {
        console.error(
          "Failed to search papers:",
          err,
        );

        setData(null);

        setError(
          err instanceof Error
            ? err.message
            : "Unable to search papers.",
        );

      } finally {
        setLoading(false);
      }

    }, [
      enabled,
      params.page,
      params.size,
      params.keyword,
      params.paper_id,
      params.year,
      params.topic,
      params.author,
    ]);

  // ==========================================================
  // Automatic fetch
  // ==========================================================
  //
  // The hook fetches ONLY when enabled=true.
  //
  // SearchPage should pass:
  //
  // enabled =
  //   hasSearched &&
  //   searchMode === "exact"
  //
  // Therefore:
  //
  // Initial page -> NO API CALL
  // Typing       -> NO API CALL
  // Exact Search -> API CALL
  // Similar      -> handled separately
  // Smart        -> handled separately
  //
  // ==========================================================

  useEffect(() => {

    if (!enabled) {
      return;
    }

    void fetchPapers();

  }, [
    enabled,
    fetchPapers,
  ]);

  // ==========================================================
  // Return
  // ==========================================================

  return {
    data,
    loading,
    error,
    refetch: fetchPapers,
  };
}