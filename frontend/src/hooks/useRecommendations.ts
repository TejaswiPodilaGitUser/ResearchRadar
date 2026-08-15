import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getSimilarPapers,
} from "../api/recommendationApi";

import type {
  RecommendationPaper,
} from "../types/recommendation";


// ============================================================
// Hook Result
// ============================================================

interface UseRecommendationsResult {
  results: RecommendationPaper[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}


// ============================================================
// Recommendations Hook
// ============================================================

export function useRecommendations(
  paperId: number | null,
  limit = 10,
): UseRecommendationsResult {

  const [results, setResults] =
    useState<RecommendationPaper[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  // ==========================================================
  // Fetch Recommendations
  // ==========================================================

  const fetchRecommendations =
    useCallback(async () => {

      // ------------------------------------------------------
      // No paper selected
      // ------------------------------------------------------

      if (paperId === null) {

        setResults([]);

        setLoading(false);

        setError(null);

        return;
      }


      // ------------------------------------------------------
      // Start loading
      // ------------------------------------------------------

      setLoading(true);

      setError(null);


      // ------------------------------------------------------
      // Fetch similar papers
      // ------------------------------------------------------

      try {

        const response =
          await getSimilarPapers(
            paperId,
            limit,
          );


        // ----------------------------------------------------
        // Store recommendation results
        // ----------------------------------------------------

        setResults(response);

      } catch (err) {

        // ----------------------------------------------------
        // Handle API error
        // ----------------------------------------------------

        const message =
          err instanceof Error
            ? err.message
            : "Unable to load similar papers.";


        setError(message);

        setResults([]);

      } finally {

        // ----------------------------------------------------
        // Stop loading
        // ----------------------------------------------------

        setLoading(false);
      }

    }, [
      paperId,
      limit,
    ]);


  // ==========================================================
  // Load When Paper ID / Limit Changes
  // ==========================================================

  useEffect(() => {

    void fetchRecommendations();

  }, [
    fetchRecommendations,
  ]);


  // ==========================================================
  // Return Hook State
  // ==========================================================

  return {
    results,
    loading,
    error,
    refetch: fetchRecommendations,
  };
}