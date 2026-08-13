import { useState } from "react";

import {
  authorApi,
  type Author,
  type AuthorDetail,
} from "../api/authorApi";

const PAGE_SIZE = 12;

export function useAuthors() {
  // ==========================================================
  // STATE
  // ==========================================================

  const [authors, setAuthors] =
    useState<Author[]>([]);

  const [selectedAuthor, setSelectedAuthor] =
    useState<AuthorDetail | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [detailLoading, setDetailLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [detailError, setDetailError] =
    useState<string | null>(null);

  const [page, setPage] =
    useState(1);

  const [total, setTotal] =
    useState(0);

  const [hasSearched, setHasSearched] =
    useState(false);

  // ==========================================================
  // SEARCH AUTHORS
  // ==========================================================

  const searchAuthors = async (
    keyword: string,
    requestedPage = 1,
  ): Promise<void> => {
    const value = keyword.trim();

    if (!value) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setDetailError(null);

      /*
       * Searching again means we are leaving
       * the current author detail view.
       */
      setSelectedAuthor(null);

      /*
       * Mark that a search has been performed.
       */
      setHasSearched(true);

      // ======================================================
      // AUTHOR ID SEARCH
      // ======================================================

      const isAuthorId =
        /^\d+$/.test(value);

      if (isAuthorId) {
        const authorId =
          Number(value);

        if (
          !Number.isSafeInteger(authorId) ||
          authorId <= 0
        ) {
          setAuthors([]);
          setTotal(0);
          setPage(1);
          setError("Invalid author ID.");
          return;
        }

        console.log(
          "Searching author by ID:",
          authorId,
        );

        const author =
          await authorApi.getAuthorById(
            authorId,
          );

        /*
         * Convert AuthorDetail into Author
         * so it can be displayed in the
         * normal search-result grid.
         */
        const authorResult: Author = {
          author_id:
            author.author_id,

          author_name:
            author.author_name,

          orcid:
            author.orcid,
        };

        setAuthors([
          authorResult,
        ]);

        setTotal(1);
        setPage(1);

        return;
      }

      // ======================================================
      // AUTHOR NAME SEARCH
      // ======================================================

      console.log(
        "Searching authors by name:",
        value,
      );

      const response =
        await authorApi.getAuthors(
          value,
          requestedPage,
          PAGE_SIZE,
        );

      console.log(
        "Authors API response:",
        response,
      );

      setAuthors(
        Array.isArray(
          response.results,
        )
          ? response.results
          : [],
      );

      setPage(
        typeof response.page ===
          "number"
          ? response.page
          : requestedPage,
      );

      setTotal(
        typeof response.total ===
          "number"
          ? response.total
          : 0,
      );
    } catch (err) {
      console.error(
        "Failed to search authors:",
        err,
      );

      setAuthors([]);
      setTotal(0);
      setPage(1);

      if (
        err instanceof Error &&
        err.message
      ) {
        setError(err.message);
      } else {
        setError(
          "Unable to find the author. Please check the name or author ID.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // LOAD AUTHOR DETAIL
  // ==========================================================

  const loadAuthor = async (
    authorId: number,
  ): Promise<void> => {
    try {
      setDetailLoading(true);
      setDetailError(null);

      console.log(
        "Loading author:",
        authorId,
      );

      const response =
        await authorApi.getAuthorById(
          authorId,
        );

      setSelectedAuthor(response);
    } catch (err) {
      console.error(
        "Failed to load author:",
        err,
      );

      setSelectedAuthor(null);

      setDetailError(
        "Unable to load this author's research papers.",
      );
    } finally {
      setDetailLoading(false);
    }
  };

  // ==========================================================
  // CLEAR SELECTED AUTHOR
  // ==========================================================

  const clearSelectedAuthor =
    (): void => {
      setSelectedAuthor(null);
      setDetailError(null);
      setDetailLoading(false);
    };

  // ==========================================================
  // CLEAR SEARCH
  // ==========================================================

  const clearAuthors =
    (): void => {
      setAuthors([]);
      setSelectedAuthor(null);

      setLoading(false);
      setDetailLoading(false);

      setError(null);
      setDetailError(null);

      setPage(1);
      setTotal(0);

      setHasSearched(false);
    };

  // ==========================================================
  // RETURN
  // ==========================================================

  return {
    authors,
    selectedAuthor,

    loading,
    detailLoading,

    error,
    detailError,

    page,
    total,
    pageSize: PAGE_SIZE,

    hasSearched,

    searchAuthors,
    loadAuthor,

    clearAuthors,
    clearSelectedAuthor,
  };
}