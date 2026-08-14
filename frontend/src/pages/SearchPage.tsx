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
import { paperApi } from "../api/paperApi";
import { searchApi } from "../api/searchApi";

import {
  SEARCH_CONFIG,
  generateYearArray,
} from "../config/search";

import type {
  PaperDetail,
  PaperListItem,
  PaperSearchParams,
} from "../types/paper";

import "../styles/search-page.css";

// ============================================================
// Types
// ============================================================

type SearchMode =
  | "keyword"
  | "semantic"
  | "hybrid";

// ============================================================
// Helpers
// ============================================================

function isNumericIdList(value: string): boolean {
  return /^\d+(?:\s*,\s*\d+)*$/.test(value);
}

function parsePaperIds(value: string): number[] {
  return [
    ...new Set(
      value
        .split(",")
        .map((item) => Number(item.trim()))
        .filter(
          (id) =>
            Number.isInteger(id) &&
            id > 0,
        ),
    ),
  ];
}

function isPaperNameList(value: string): boolean {
  return value.includes(",");
}

function parsePaperNames(value: string): string[] {
  return [
    ...new Set(
      value
        .split(",")
        .map((name) => name.trim())
        .filter(Boolean),
    ),
  ];
}

function paperDetailToListItem(
  paper: PaperDetail,
): PaperListItem {
  return paper as PaperListItem;
}

// ============================================================
// Search Page
// ============================================================

function SearchPage() {
  const navigate = useNavigate();

  // ==========================================================
  // Search state
  // ==========================================================

  const [keyword, setKeyword] = useState("");

  const [year, setYear] =
    useState<number | undefined>();

  const [topic, setTopic] =
    useState("");

  const [author, setAuthor] =
    useState("");

  const [page, setPage] = useState(1);

  const [searchMode, setSearchMode] =
    useState<SearchMode>("keyword");

  /*
   * Search is disabled initially.
   *
   * Therefore the page does NOT fetch
   * /api/papers on initial load.
   */
  const [hasSearched, setHasSearched] =
    useState(false);

  // ==========================================================
  // Search results
  // ==========================================================

  const [searchResults, setSearchResults] =
    useState<PaperListItem[] | null>(null);

  const [searchLoading, setSearchLoading] =
    useState(false);

  const [searchError, setSearchError] =
    useState<string | null>(null);

  // ==========================================================
  // Exact / keyword search parameters
  // ==========================================================

  /*
   * Normal keyword/filter searches still use usePapers.
   *
   * ID and paper-name searches are handled separately
   * by handleSearch().
   */
  const searchParams =
    useMemo<PaperSearchParams>(() => {
      return {
        page,
        size: SEARCH_CONFIG.PAGE_SIZE,

        keyword:
          keyword.trim() || undefined,

        year:
          year ?? undefined,

        topic:
          topic.trim() || undefined,

        author:
          author.trim() || undefined,
      };
    }, [
      page,
      keyword,
      year,
      topic,
      author,
    ]);

  // ==========================================================
  // Normal keyword search
  // ==========================================================

  const {
    data,
    loading: papersLoading,
    error: papersError,
    refetch,
  } = usePapers(
    searchParams,
    hasSearched &&
      searchMode === "keyword" &&
      !isNumericIdList(keyword.trim()) &&
      !isPaperNameList(keyword.trim()),
  );

  // ==========================================================
  // Years
  // ==========================================================

  const years = useMemo(
    () =>
      generateYearArray(
        SEARCH_CONFIG.CURRENT_YEAR,
        SEARCH_CONFIG.YEARS_RANGE,
      ),
    [],
  );

  // ==========================================================
  // Search mode
  // ==========================================================

  const isAiSearch =
    searchMode === "semantic" ||
    searchMode === "hybrid";

  // ==========================================================
  // Execute ID / Name / AI Search
  // ==========================================================

  const executeSearch =
    async (): Promise<void> => {
      const value = keyword.trim();

      if (!value) {
        setSearchResults(null);
        setSearchError(
          "Please enter a Paper ID, paper name, keyword, or research concept.",
        );
        return;
      }

      setSearchLoading(true);
      setSearchError(null);
      setSearchResults(null);

      try {
        // ======================================================
        // PAPER ID SEARCH
        // ======================================================

        if (
          searchMode === "keyword" &&
          isNumericIdList(value)
        ) {
          const ids =
            parsePaperIds(value);

          if (ids.length === 0) {
            throw new Error(
              "Please enter a valid Paper ID.",
            );
          }

          let results: PaperListItem[] = [];

          // ----------------------------------------------------
          // Single ID
          // ----------------------------------------------------

          if (ids.length === 1) {
            const paper =
              await paperApi.getPaperById(
                ids[0],
              );

            results = [
              paperDetailToListItem(
                paper,
              ),
            ];
          }

          // ----------------------------------------------------
          // Multiple IDs
          // ----------------------------------------------------

          else {
            const response =
              await paperApi.getPapersByIds(
                ids,
              );

            results =
              response.results ?? [];
          }

          setSearchResults(results);
          return;
        }

        // ======================================================
        // PAPER NAME SEARCH
        // ======================================================

        if (
          searchMode === "keyword" &&
          isPaperNameList(value)
        ) {
          const names =
            parsePaperNames(value);

          if (names.length === 0) {
            throw new Error(
              "Please enter a valid paper name.",
            );
          }

          let results: PaperListItem[] = [];

          // ----------------------------------------------------
          // Single name
          // ----------------------------------------------------

          if (names.length === 1) {
            const paper =
              await paperApi.getPaperByName(
                names[0],
              );

            results = [
              paperDetailToListItem(
                paper,
              ),
            ];
          }

          // ----------------------------------------------------
          // Multiple names
          // ----------------------------------------------------

          else {
            const response =
              await paperApi.getPapersByNames(
                names,
              );

            results =
              response.results ?? [];
          }

          setSearchResults(results);
          return;
        }

        // ======================================================
        // SEMANTIC SEARCH
        // ======================================================

        if (searchMode === "semantic") {
          const results =
            await searchApi.semanticSearch({
              query: value,
              limit:
                SEARCH_CONFIG.MAX_SEARCH_RESULTS,
            });

          setSearchResults(
            Array.isArray(results)
              ? results
              : [],
          );

          return;
        }

        // ======================================================
        // HYBRID / SMART SEARCH
        // ======================================================

        if (searchMode === "hybrid") {
          const results =
            await searchApi.hybridSearch({
              query: value,
              limit:
                SEARCH_CONFIG.MAX_SEARCH_RESULTS,
            });

          setSearchResults(
            Array.isArray(results)
              ? results
              : [],
          );

          return;
        }

        // ======================================================
        // NORMAL KEYWORD SEARCH
        // ======================================================

        /*
         * Normal keyword search is performed by usePapers.
         *
         * Nothing is required here.
         */
      } catch (error) {
        console.error(
          "Search failed:",
          error,
        );

        setSearchResults(null);

        setSearchError(
          error instanceof Error
            ? error.message
            : "Unable to perform the search. Please try again.",
        );
      } finally {
        setSearchLoading(false);
      }
    };

  // ==========================================================
  // Search
  // ==========================================================

  const handleSearch = (): void => {
    const value = keyword.trim();

    if (!value) {
      setHasSearched(false);
      setSearchResults(null);

      setSearchError(
        "Please enter a Paper ID, paper name, keyword, or research concept.",
      );

      return;
    }

    // --------------------------------------------------------
    // Reset previous state
    // --------------------------------------------------------

    setPage(1);
    setSearchError(null);
    setSearchResults(null);

    // --------------------------------------------------------
    // Enable search
    // --------------------------------------------------------

    setHasSearched(true);

    // --------------------------------------------------------
    // ID / Name / AI searches
    // --------------------------------------------------------

    if (
      searchMode === "semantic" ||
      searchMode === "hybrid" ||
      isNumericIdList(value) ||
      isPaperNameList(value)
    ) {
      void executeSearch();
    }

    // --------------------------------------------------------
    // Normal keyword search
    // --------------------------------------------------------

    /*
     * usePapers automatically executes because:
     *
     * hasSearched = true
     *
     * and its enabled flag becomes true.
     */
  };

  // ==========================================================
  // Search Mode Change
  // ==========================================================

  const handleSearchModeChange = (
    mode: SearchMode,
  ): void => {
    setSearchMode(mode);

    setHasSearched(false);

    setSearchResults(null);
    setSearchError(null);

    setPage(1);
  };

  // ==========================================================
  // Keyword Change
  // ==========================================================

  const handleKeywordChange = (
    value: string,
  ): void => {
    setKeyword(value);

    /*
     * User must press Search again.
     */
    setHasSearched(false);

    setSearchResults(null);
    setSearchError(null);

    setPage(1);
  };

  // ==========================================================
  // Year Change
  // ==========================================================

  const handleYearChange = (
    value?: number,
  ): void => {
    setYear(value);

    setHasSearched(false);

    setSearchResults(null);
    setSearchError(null);

    setPage(1);
  };

  // ==========================================================
  // Topic Change
  // ==========================================================

  const handleTopicChange = (
    value: string,
  ): void => {
    setTopic(value);

    setHasSearched(false);

    setSearchResults(null);
    setSearchError(null);

    setPage(1);
  };

  // ==========================================================
  // Author Change
  // ==========================================================

  const handleAuthorChange = (
    value: string,
  ): void => {
    setAuthor(value);

    setHasSearched(false);

    setSearchResults(null);
    setSearchError(null);

    setPage(1);
  };

  // ==========================================================
  // Clear Search
  // ==========================================================

  const handleClearSearch =
    (): void => {
      setKeyword("");

      setYear(undefined);

      setTopic("");

      setAuthor("");

      setPage(1);

      setHasSearched(false);

      setSearchResults(null);

      setSearchError(null);
    };

  // ==========================================================
  // Paper Selection
  // ==========================================================

  const handlePaperSelect = (
    paperId: number,
  ): void => {
    navigate(
      `/papers/${paperId}`,
    );
  };

  // ==========================================================
  // Search State
  // ==========================================================

  const hasFilters =
    year !== undefined ||
    Boolean(topic.trim()) ||
    Boolean(author.trim());

  const hasSearchInput =
    Boolean(keyword.trim()) ||
    hasFilters;

  const activeFilterCount =
    Number(year !== undefined) +
    Number(Boolean(topic.trim())) +
    Number(Boolean(author.trim()));

  // ==========================================================
  // Determine Special Search
  // ==========================================================

  const isSpecialKeywordSearch =
    searchMode === "keyword" &&
    (
      isNumericIdList(
        keyword.trim(),
      ) ||
      isPaperNameList(
        keyword.trim(),
      )
    );

  // ==========================================================
  // Current Loading State
  // ==========================================================

  const loading =
    isAiSearch ||
    isSpecialKeywordSearch
      ? searchLoading
      : papersLoading;

  // ==========================================================
  // Current Error
  // ==========================================================

  const error =
    searchError ??
    (
      isAiSearch ||
      isSpecialKeywordSearch
        ? null
        : papersError
    );

  // ==========================================================
  // Current Results
  // ==========================================================

  const results =
    isAiSearch ||
    isSpecialKeywordSearch
      ? searchResults ?? []
      : data?.results ?? [];

  // ==========================================================
  // Total
  // ==========================================================

  const total =
    isAiSearch ||
    isSpecialKeywordSearch
      ? results.length
      : data?.total ?? 0;

  // ==========================================================
  // Results Title
  // ==========================================================

  const getResultsTitle =
    (): string => {
      if (
        searchMode === "semantic"
      ) {
        return "Similar Papers";
      }

      if (
        searchMode === "hybrid"
      ) {
        return "Smart Search Results";
      }

      if (
        isNumericIdList(
          keyword.trim(),
        )
      ) {
        return "Paper ID Results";
      }

      if (
        isPaperNameList(
          keyword.trim(),
        )
      ) {
        return "Paper Name Results";
      }

      return "Exact Search Results";
    };

  // ==========================================================
  // Loading Message
  // ==========================================================

  const getLoadingMessage =
    (): string => {
      if (
        searchMode === "semantic"
      ) {
        return "Finding similar papers...";
      }

      if (
        searchMode === "hybrid"
      ) {
        return "Finding the best matches...";
      }

      return "Searching research papers...";
    };

  // ==========================================================
  // Empty Message
  // ==========================================================

  const getEmptyMessage =
    (): string => {
      if (
        searchMode === "semantic"
      ) {
        return "No similar papers were found. Try another research concept.";
      }

      if (
        searchMode === "hybrid"
      ) {
        return "No relevant papers were found. Try changing your search.";
      }

      if (
        isNumericIdList(
          keyword.trim(),
        )
      ) {
        return "No papers were found for the specified Paper ID(s).";
      }

      if (
        isPaperNameList(
          keyword.trim(),
        )
      ) {
        return "No papers were found for the specified paper name(s).";
      }

      return "No papers matched your search. Try another title, keyword, author, topic, or year.";
    };

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <main className="search-page">

      {/* ====================================================
          Hero
          ==================================================== */}

      <section className="search-hero">

        <div className="search-hero-content">

          <div className="search-eyebrow">
            RESEARCH DISCOVERY
          </div>

          <h1>
            Research Papers
          </h1>

          <p>
            Search and explore research
            papers across the Research
            Radar corpus.
          </p>

        </div>

      </section>

      {/* ====================================================
          Search
          ==================================================== */}

      <section className="search-area">

        <div className="search-panel">

          {/* ------------------------------------------------
              Header
              ------------------------------------------------ */}

          <div className="search-panel-header">

            <div>

              <h2>
                Search Research Papers
              </h2>

              <p>
                Search by Paper ID,
                paper name, title,
                abstract, topic,
                author, or year.
              </p>

            </div>

            {activeFilterCount > 0 && (
              <span className="filter-count">

                {activeFilterCount}{" "}

                {activeFilterCount === 1
                  ? "filter"
                  : "filters"}{" "}

                applied

              </span>
            )}

          </div>

          {/* ------------------------------------------------
              Search Bar
              ------------------------------------------------ */}

          <div className="search-input-wrapper">

            <SearchBar
              value={keyword}
              onChange={
                handleKeywordChange
              }
              placeholder="Search by Paper ID, paper name, keywords, or research concepts..."
              searchMode={searchMode}
              onSearchModeChange={
                handleSearchModeChange
              }
            />

            <button
              type="button"
              className="search-button"
              onClick={handleSearch}
            >
              Search
            </button>

          </div>

          {/* ------------------------------------------------
              Filters
              ------------------------------------------------ */}

          <div className="filters-wrapper">

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
                handleClearSearch
              }
            />

          </div>

        </div>

      </section>

      {/* ====================================================
          Results
          ==================================================== */}

      <section
        className="results-section"
        aria-label="Research papers"
      >

        {/* ------------------------------------------------
            Initial State
            ------------------------------------------------ */}

        {!hasSearched &&
          !loading && (
            <EmptyState
              title="Start exploring research"
              message="Enter a Paper ID, paper name, keyword, or research concept and choose a search type."
            />
          )}

        {/* ------------------------------------------------
            Results Header
            ------------------------------------------------ */}

        {hasSearched &&
          !loading &&
          !error && (
            <div className="results-header">

              <div>

                <h2>
                  {getResultsTitle()}
                </h2>

                <p className="results-description">

                  {total.toLocaleString()}{" "}

                  {total === 1
                    ? "paper"
                    : "papers"}{" "}

                  found

                </p>

              </div>

              {hasSearchInput && (
                <button
                  type="button"
                  className="clear-search-button"
                  onClick={
                    handleClearSearch
                  }
                >
                  Clear Search
                </button>
              )}

            </div>
          )}

        {/* ------------------------------------------------
            Loading
            ------------------------------------------------ */}

        {loading && (
          <LoadingState
            message={
              getLoadingMessage()
            }
          />
        )}

        {/* ------------------------------------------------
            Error
            ------------------------------------------------ */}

        {!loading &&
          error && (
            <ErrorState
              message={error}
              onRetry={
                isAiSearch ||
                isSpecialKeywordSearch
                  ? executeSearch
                  : refetch
              }
            />
          )}

        {/* ------------------------------------------------
            No Results
            ------------------------------------------------ */}

        {hasSearched &&
          !loading &&
          !error &&
          results.length === 0 && (
            <EmptyState
              title="No papers found"
              message={
                getEmptyMessage()
              }
            />
          )}

        {/* ------------------------------------------------
            Results
            ------------------------------------------------ */}

        {!loading &&
          !error &&
          results.length > 0 && (
            <>
              <PaperList
                papers={results}
                onPaperClick={
                  handlePaperSelect
                }
              />

              {/* --------------------------------------------
                  Pagination only for normal keyword search
                  -------------------------------------------- */}

              {!isAiSearch &&
                !isSpecialKeywordSearch &&
                data && (
                  <Pagination
                    page={data.page}
                    pageSize={
                      data.page_size
                    }
                    total={data.total}
                    onPageChange={
                      setPage
                    }
                  />
                )}
            </>
          )}

      </section>

    </main>
  );
}

export default SearchPage;