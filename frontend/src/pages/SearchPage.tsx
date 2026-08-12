import { useMemo, useState } from "react";

import { useNavigate } from "react-router-dom";

import SearchBar from "../components/search/SearchBar";
import SearchFilters from "../components/search/SearchFilters";

import PaperList from "../components/papers/PaperList";

import { LoadingState } from "../components/common/LoadingState";
import { ErrorState } from "../components/common/ErrorState";
import { EmptyState } from "../components/common/EmptyState";
import { Pagination } from "../components/common/Pagination";

import { usePapers } from "../hooks/usePapers";
import { useDebounce } from "../hooks/useDebounce";
import {
  SEARCH_CONFIG,
  generateYearArray,
} from "../config/search";

import type {
  PaperSearchParams,
} from "../types/paper";

// ============================================================
// Search Page
// ============================================================

export function SearchPage() {
  const navigate = useNavigate();

  // ----------------------------------------------------------
  // Search state
  // ----------------------------------------------------------

  const [keyword, setKeyword] =
    useState("");

  const [year, setYear] =
    useState<number | undefined>(undefined);

  const [topic, setTopic] =
    useState("");

  const [author, setAuthor] =
    useState("");

  const [page, setPage] =
    useState(1);

  // ----------------------------------------------------------
  // Debounce search input
  // ----------------------------------------------------------

  const debouncedKeyword =
    useDebounce(
      keyword,
      SEARCH_CONFIG.DEBOUNCE_DELAY,
    );

  const debouncedTopic =
    useDebounce(
      topic,
      SEARCH_CONFIG.DEBOUNCE_DELAY,
    );

  const debouncedAuthor =
    useDebounce(
      author,
      SEARCH_CONFIG.DEBOUNCE_DELAY,
    );

  // ----------------------------------------------------------
  // Build API parameters
  // ----------------------------------------------------------

  const searchParams =
    useMemo<PaperSearchParams>(
      () => ({
        page,
        size: SEARCH_CONFIG.PAGE_SIZE,

        keyword:
          debouncedKeyword.trim() ||
          undefined,

        topic:
          debouncedTopic.trim() ||
          undefined,

        author:
          debouncedAuthor.trim() ||
          undefined,

        year: year || undefined,
      }),
      [
        page,
        debouncedKeyword,
        debouncedTopic,
        debouncedAuthor,
        year,
      ]
    );

  // ----------------------------------------------------------
  // Fetch papers
  // ----------------------------------------------------------

  const {
    data,
    loading,
    error,
    refetch,
  } = usePapers(searchParams);

  // ----------------------------------------------------------
  // Handlers
  // ----------------------------------------------------------

  const handleKeywordChange = (
    value: string
  ) => {
    setKeyword(value);
    setPage(1);
  };

  const handleYearChange = (
    value?: number
  ) => {
    setYear(value);
    setPage(1);
  };

  const handleTopicChange = (
    value: string
  ) => {
    setTopic(value);
    setPage(1);
  };

  const handleAuthorChange = (
    value: string
  ) => {
    setAuthor(value);
    setPage(1);
  };

  const handleClearFilters =
    () => {
      setKeyword("");
      setYear(undefined);
      setTopic("");
      setAuthor("");
      setPage(1);
    };

  const handlePaperSelect = (
    paperId: number
  ) => {
    navigate(
      `/papers/${paperId}`
    );
  };

  // ----------------------------------------------------------
  // Generate available years
  // ----------------------------------------------------------

  const years = useMemo(
    () => generateYearArray(
      SEARCH_CONFIG.CURRENT_YEAR,
      SEARCH_CONFIG.YEARS_RANGE,
    ),
    [],
  );

  // ----------------------------------------------------------
  // Render
  // ----------------------------------------------------------

  return (
    <div className="page">
      <section className="hero">
        <h1>Research Radar</h1>

        <p>
          Discover and explore
          research papers.
        </p>
      </section>

      <div className="search-panel">
        <div className="search-row">
          <SearchBar
            value={keyword}
            onChange={
              handleKeywordChange
            }
          />
        </div>

        <SearchFilters
          year={year}
          topic={topic}
          author={author}
          years={years}
          onYearChange={
            handleYearChange
          }
          onTopicChange={
            handleTopicChange
          }
          onAuthorChange={
            handleAuthorChange
          }
          onClear={
            handleClearFilters
          }
        />
      </div>

      <section
        className="results-section"
        aria-label="Search results"
      >
        {loading && (
          <LoadingState
            message="Searching research papers..."
          />
        )}

        {!loading && error && (
          <ErrorState
            message={error}
            onRetry={refetch}
          />
        )}

        {!loading &&
          !error &&
          data?.results?.length === 0 && (
            <EmptyState
              title="No papers found"
              message="Try a different keyword, topic, author, or publication year."
            />
          )}

        {!loading &&
          !error &&
          data?.results?.length! > 0 && (
            <>
              <div className="results-summary">
                <span>
                  {data?.total}{" "}
                  {data?.total === 1
                    ? "paper"
                    : "papers"}{" "}
                  found
                </span>
              </div>

              <PaperList
                papers={data?.results ?? []}
                onPaperClick={
                  handlePaperSelect
                }
              />

              <Pagination
                page={data?.page ?? 1}
                pageSize={
                  data?.page_size ?? 20
                }
                total={data?.total ?? 0}
                onPageChange={
                  setPage
                }
              />
            </>
          )}
      </section>
    </div>
  );
}

export default SearchPage;