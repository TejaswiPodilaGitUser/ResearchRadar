import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import SearchBar from "../components/search/SearchBar";
import SearchFilters from "../components/search/SearchFilters";
import SearchTabs from "../components/search/SearchTabs";
import PaperList from "../components/papers/PaperList";

import { LoadingState } from "../components/common/LoadingState";
import { ErrorState } from "../components/common/ErrorState";
import { EmptyState } from "../components/common/EmptyState";
import { Pagination } from "../components/common/Pagination";

import { usePapers } from "../hooks/usePapers";
import { useDebounce } from "../hooks/useDebounce";

import { searchApi } from "../api/searchApi";

import {
  SEARCH_CONFIG,
  generateYearArray,
} from "../config/search";

import type {
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

type SearchTab =
  | "papers"
  | "authors"
  | "topics";

// ============================================================
// Helper Functions
// ============================================================

function getResultsTitle(
  hasSearch: boolean,
  searchMode: SearchMode,
): string {
  if (!hasSearch) {
    return "Research Papers";
  }

  if (searchMode === "semantic") {
    return "Similar Papers";
  }

  if (searchMode === "hybrid") {
    return "Smart Search Results";
  }

  return "Search Results";
}

function getLoadingMessage(
  searchMode: SearchMode,
): string {
  if (searchMode === "semantic") {
    return "Finding similar papers...";
  }

  if (searchMode === "hybrid") {
    return "Finding the best matches...";
  }

  return "Searching research papers...";
}

function getEmptyMessage(
  isAiSearch: boolean,
): string {
  if (isAiSearch) {
    return "Try another research question or search phrase.";
  }

  return "Try a different keyword, topic, author, or publication year.";
}

function getSearchPlaceholder(
  activeTab: SearchTab,
): string {
  if (activeTab === "authors") {
    return "Search by author name or author ID...";
  }

  if (activeTab === "topics") {
    return "Search by topic name or topic ID...";
  }

  return "Search by title, paper ID, author, topic, keywords, or research concepts...";
}

function getTabResultsTitle(
  activeTab: SearchTab,
): string {
  if (activeTab === "authors") {
    return "Authors";
  }

  if (activeTab === "topics") {
    return "Topics";
  }

  return "Research Papers";
}

// ============================================================
// Search Page
// ============================================================

export function SearchPage() {
  const navigate = useNavigate();

  // ----------------------------------------------------------
  // Search state
  // ----------------------------------------------------------

  const [activeTab, setActiveTab] =
    useState<SearchTab>("papers");

  const [keyword, setKeyword] = useState("");

  const [year, setYear] =
    useState<number | undefined>(undefined);

  const [topic, setTopic] = useState("");

  const [author, setAuthor] = useState("");

  const [page, setPage] = useState(1);

  const [searchMode, setSearchMode] =
    useState<SearchMode>("keyword");

  // ----------------------------------------------------------
  // AI search state
  // ----------------------------------------------------------

  const [aiResults, setAiResults] =
    useState<PaperListItem[] | null>(null);

  const [aiLoading, setAiLoading] =
    useState(false);

  const [aiError, setAiError] =
    useState<string | null>(null);

  // ----------------------------------------------------------
  // Debounced values
  // ----------------------------------------------------------

  const debouncedKeyword = useDebounce(
    keyword,
    SEARCH_CONFIG.DEBOUNCE_DELAY,
  );

  const debouncedTopic = useDebounce(
    topic,
    SEARCH_CONFIG.DEBOUNCE_DELAY,
  );

  const debouncedAuthor = useDebounce(
    author,
    SEARCH_CONFIG.DEBOUNCE_DELAY,
  );

  // ----------------------------------------------------------
  // Normal paper search parameters
  // ----------------------------------------------------------

  const searchParams = useMemo<PaperSearchParams>(
    () => ({
      page,
      size: SEARCH_CONFIG.PAGE_SIZE,

      keyword:
        debouncedKeyword.trim() || undefined,

      topic:
        debouncedTopic.trim() || undefined,

      author:
        debouncedAuthor.trim() || undefined,

      year: year || undefined,
    }),
    [
      page,
      debouncedKeyword,
      debouncedTopic,
      debouncedAuthor,
      year,
    ],
  );

  // ----------------------------------------------------------
  // Normal paper search
  // ----------------------------------------------------------

  const {
    data,
    loading: papersLoading,
    error: papersError,
    refetch,
  } = usePapers(searchParams);

  // ----------------------------------------------------------
  // Search mode
  // ----------------------------------------------------------

  const isAiSearch =
    searchMode === "semantic" ||
    searchMode === "hybrid";

  // ----------------------------------------------------------
  // Execute AI search
  // ----------------------------------------------------------

  const executeAiSearch = async (
    mode: SearchMode,
  ): Promise<void> => {
    const query = keyword.trim();

    if (!query || mode === "keyword") {
      setAiResults(null);
      return;
    }

    setAiLoading(true);
    setAiError(null);

    try {
      let results: PaperListItem[];

      if (mode === "semantic") {
        results =
          await searchApi.semanticSearch({
            query,
            limit:
              SEARCH_CONFIG.MAX_SEARCH_RESULTS,
          });
      } else {
        results =
          await searchApi.hybridSearch({
            query,
            limit:
              SEARCH_CONFIG.MAX_SEARCH_RESULTS,
          });
      }

      setAiResults(results);
    } catch (error) {
      console.error(
        `Failed to perform ${mode} search`,
        error,
      );

      setAiError(
        "Unable to perform this search. Please try again.",
      );

      setAiResults(null);
    } finally {
      setAiLoading(false);
    }
  };

  // ----------------------------------------------------------
  // Handlers
  // ----------------------------------------------------------

  const handleTabChange = (
    tab: SearchTab,
  ): void => {
    setActiveTab(tab);

    setKeyword("");
    setPage(1);

    setAiResults(null);
    setAiError(null);

    /*
     * Search filters belong to the Papers
     * tab only. They are intentionally kept
     * separate from Author and Topic search.
     */
    if (tab !== "papers") {
      setYear(undefined);
      setTopic("");
      setAuthor("");
    }
  };

  const handleKeywordChange = (
    value: string,
  ): void => {
    setKeyword(value);
    setPage(1);

    if (!value.trim()) {
      setAiResults(null);
      setAiError(null);
    }
  };

  const handleSearchModeChange = (
    mode: SearchMode,
  ): void => {
    setSearchMode(mode);
    setPage(1);

    setAiResults(null);
    setAiError(null);

    if (
      mode !== "keyword" &&
      keyword.trim()
    ) {
      void executeAiSearch(mode);
    }
  };

  const handleYearChange = (
    value?: number,
  ): void => {
    setYear(value);
    setPage(1);
  };

  const handleTopicChange = (
    value: string,
  ): void => {
    setTopic(value);
    setPage(1);
  };

  const handleAuthorChange = (
    value: string,
  ): void => {
    setAuthor(value);
    setPage(1);
  };

  const handleClearFilters = (): void => {
    setKeyword("");
    setYear(undefined);
    setTopic("");
    setAuthor("");
    setPage(1);

    setAiResults(null);
    setAiError(null);
  };

  const handlePaperSelect = (
    paperId: number,
  ): void => {
    navigate(`/papers/${paperId}`);
  };

  // ----------------------------------------------------------
  // Available years
  // ----------------------------------------------------------

  const years = useMemo(
    () =>
      generateYearArray(
        SEARCH_CONFIG.CURRENT_YEAR,
        SEARCH_CONFIG.YEARS_RANGE,
      ),
    [],
  );

  // ----------------------------------------------------------
  // Search state
  // ----------------------------------------------------------

  const activeFilterCount =
    Number(Boolean(year)) +
    Number(Boolean(topic.trim())) +
    Number(Boolean(author.trim()));

  const hasSearch =
    Boolean(keyword.trim()) ||
    Boolean(topic.trim()) ||
    Boolean(author.trim()) ||
    Boolean(year);

  // ----------------------------------------------------------
  // Current results
  // ----------------------------------------------------------

  const currentResults = isAiSearch
    ? aiResults ?? []
    : data?.results ?? [];

  const totalResults = isAiSearch
    ? currentResults.length
    : data?.total ?? 0;

  const isLoading = isAiSearch
    ? aiLoading
    : papersLoading;

  const currentError = isAiSearch
    ? aiError
    : papersError;

  const resultsTitle =
    activeTab === "papers"
      ? getResultsTitle(
          hasSearch,
          searchMode,
        )
      : getTabResultsTitle(activeTab);

  const loadingMessage =
    getLoadingMessage(searchMode);

  const emptyMessage =
    getEmptyMessage(isAiSearch);

  const searchPlaceholder =
    getSearchPlaceholder(activeTab);

  // ----------------------------------------------------------
  // Render
  // ----------------------------------------------------------

  return (
    <main className="search-page">

      {/* ======================================================
          Hero
          ====================================================== */}

      <section className="search-hero">
        <div className="search-hero-content">

          <div className="search-eyebrow">
            RESEARCH DISCOVERY
          </div>

          <h1>
            Discover Research.
            <br />
            Explore Ideas.
          </h1>

          <p>
            Search and explore research papers,
            authors, and topics across the
            Research Radar corpus.
          </p>

        </div>
      </section>

      {/* ======================================================
          Search Area
          ====================================================== */}

      <section className="search-area">

        <div className="search-panel">

          {/* --------------------------------------------------
              Header
              -------------------------------------------------- */}

          <div className="search-panel-header">

            <div>
              <h2>
                Search Research
              </h2>

              <p>
                Search by title, paper ID,
                author, topic, keywords,
                or research concepts.
              </p>
            </div>

            {activeFilterCount > 0 &&
              activeTab === "papers" && (
                <span className="filter-count">
                  {activeFilterCount}{" "}
                  {activeFilterCount === 1
                    ? "filter"
                    : "filters"}{" "}
                  applied
                </span>
              )}

          </div>

          {/* --------------------------------------------------
              Main Search Tabs
              -------------------------------------------------- */}

          <SearchTabs
            activeTab={activeTab}
            onTabChange={handleTabChange}
          />

          {/* ==================================================
              PAPERS SEARCH
              ================================================== */}

          {activeTab === "papers" && (
            <>
              <div className="search-input-wrapper">

                <SearchBar
                  value={keyword}
                  onChange={
                    handleKeywordChange
                  }
                  searchMode={
                    searchMode
                  }
                  onSearchModeChange={
                    handleSearchModeChange
                  }
                  placeholder={
                    searchPlaceholder
                  }
                />

              </div>

              {/* ----------------------------------------------
                  Paper Filters
                  ---------------------------------------------- */}

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
                    handleClearFilters
                  }
                />

              </div>
            </>
          )}

          {/* ==================================================
              AUTHORS SEARCH
              ================================================== */}

          {activeTab === "authors" && (
            <div className="entity-search-panel">

              <div className="entity-search-info">
                <span className="entity-search-icon">
                  👤
                </span>

                <div>
                  <h3>
                    Search Authors
                  </h3>

                  <p>
                    Find researchers by name
                    or author identifier.
                  </p>
                </div>
              </div>

              <div className="entity-search-placeholder">
                Author search API and results
                will be connected here.
              </div>

            </div>
          )}

          {/* ==================================================
              TOPICS SEARCH
              ================================================== */}

          {activeTab === "topics" && (
            <div className="entity-search-panel">

              <div className="entity-search-info">
                <span className="entity-search-icon">
                  🏷
                </span>

                <div>
                  <h3>
                    Search Topics
                  </h3>

                  <p>
                    Find research topics by
                    name or topic identifier.
                  </p>
                </div>
              </div>

              <div className="entity-search-placeholder">
                Topic search API and results
                will be connected here.
              </div>

            </div>
          )}

        </div>

      </section>

      {/* ======================================================
          Results
          ====================================================== */}

      <section
        className="results-section"
        aria-label="Search results"
      >

        {/* --------------------------------------------------
            Results Header
            -------------------------------------------------- */}

        {!isLoading &&
          !currentError && (
            <div className="results-header">

              <div>

                <h2>
                  {resultsTitle}
                </h2>

                <p className="results-description">
                  {totalResults.toLocaleString()}{" "}
                  {totalResults === 1
                    ? "paper"
                    : "papers"}{" "}
                  available
                </p>

              </div>

              {hasSearch &&
                activeTab === "papers" && (
                  <button
                    type="button"
                    className="clear-search-button"
                    onClick={
                      handleClearFilters
                    }
                  >
                    Clear Search
                  </button>
                )}

            </div>
          )}

        {/* --------------------------------------------------
            Loading
            -------------------------------------------------- */}

        {isLoading && (
          <LoadingState
            message={loadingMessage}
          />
        )}

        {/* --------------------------------------------------
            Error
            -------------------------------------------------- */}

        {!isLoading &&
          currentError && (
            <ErrorState
              message={currentError}
              onRetry={
                isAiSearch
                  ? () =>
                      void executeAiSearch(
                        searchMode,
                      )
                  : refetch
              }
            />
          )}

        {/* --------------------------------------------------
            Empty
            -------------------------------------------------- */}

        {!isLoading &&
          !currentError &&
          activeTab === "papers" &&
          currentResults.length === 0 && (
            <EmptyState
              title="No papers found"
              message={emptyMessage}
            />
          )}

        {/* --------------------------------------------------
            Paper Results
            -------------------------------------------------- */}

        {!isLoading &&
          !currentError &&
          activeTab === "papers" &&
          currentResults.length > 0 && (
            <>
              <PaperList
                papers={currentResults}
                onPaperClick={
                  handlePaperSelect
                }
              />

              {!isAiSearch && (
                <Pagination
                  page={
                    data?.page ?? 1
                  }
                  pageSize={
                    data?.page_size ??
                    SEARCH_CONFIG.PAGE_SIZE
                  }
                  total={
                    data?.total ?? 0
                  }
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

