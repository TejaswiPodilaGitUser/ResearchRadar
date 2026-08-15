import {
  useState,
  type KeyboardEvent,
} from "react";

import { useNavigate } from "react-router-dom";

import { useAuthors } from "../hooks/useAuthors";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";

import "../styles/entity-page.css";
import "../styles/author-page.css";


/* ============================================================
   HELPERS
   ============================================================ */

function getInitials(
  name: string,
): string {
  const parts = name
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  if (parts.length === 0) {
    return "?";
  }

  return parts
    .slice(0, 2)
    .map((part) =>
      part.charAt(0).toUpperCase(),
    )
    .join("");
}


/* ============================================================
   AUTHORS PAGE
   ============================================================ */

function AuthorsPage() {
  const navigate = useNavigate();

  const [search, setSearch] =
    useState("");

  const {
    authors,
    selectedAuthor,

    loading,
    detailLoading,

    error,
    detailError,

    page,
    total,
    pageSize,

    hasSearched,

    searchAuthors,
    loadAuthor,

    clearAuthors,
    clearSelectedAuthor,
  } = useAuthors();


  /* ==========================================================
     SEARCH
     ========================================================== */

  const handleSearch = (): void => {
    const keyword =
      search.trim();

    if (
      !keyword ||
      loading
    ) {
      return;
    }

    void searchAuthors(
      keyword,
      1,
    );
  };


  const handleKeyDown = (
    event: KeyboardEvent<HTMLInputElement>,
  ): void => {
    if (event.key === "Enter") {
      event.preventDefault();

      handleSearch();
    }
  };


  const handleClear = (): void => {
    setSearch("");

    clearAuthors();
  };


  /* ==========================================================
     AUTHOR ACTIONS
     ========================================================== */

  const handleAuthorClick = (
    authorId: number,
  ): void => {
    void loadAuthor(authorId);
  };


  const handleBack = (): void => {
    clearSelectedAuthor();
  };


  /* ==========================================================
     PAGINATION
     ========================================================== */

  const totalPages =
    pageSize > 0
      ? Math.ceil(
          total / pageSize,
        )
      : 0;


  /*
   * ==========================================================
   * AUTHOR DETAIL VIEW
   * ==========================================================
   */

  if (selectedAuthor) {
    const papers =
      selectedAuthor.papers ?? [];

    return (
      <main className="author-page">

        <div className="author-page-container">

          {/* ==================================================
              DETAIL HEADER
              ================================================== */}

          <section className="author-page-header">

            <div className="author-page-eyebrow">
              RESEARCHER
            </div>

            <h1>
              {selectedAuthor.author_name}
            </h1>

            <p>
              Research profile and
              published research papers.
            </p>

          </section>


          {/* ==================================================
              BACK BUTTON
              ================================================== */}

          <button
            type="button"
            className="author-clear-button"
            onClick={handleBack}
          >
            ← Back to Authors
          </button>


          {/* ==================================================
              AUTHOR PROFILE
              ================================================== */}

          <section className="author-detail-card">

            <div className="author-detail-avatar">
              {getInitials(
                selectedAuthor.author_name,
              )}
            </div>

            <div className="author-detail-content">

              <div className="author-page-eyebrow">
                RESEARCHER
              </div>

              <h2>
                {selectedAuthor.author_name}
              </h2>

              <div className="author-detail-meta">

                <span>
                  <span className="author-detail-meta-label">
                    Author ID
                  </span>

                  <strong>
                    {selectedAuthor.author_id}
                  </strong>
                </span>

                {selectedAuthor.orcid && (
                  <span>
                    <span className="author-detail-meta-label">
                      ORCID
                    </span>

                    <strong>
                      {selectedAuthor.orcid}
                    </strong>
                  </span>
                )}

              </div>

            </div>

          </section>


          {/* ==================================================
              RESEARCH PAPERS
              ================================================== */}

          <section className="author-detail-papers">

            <div className="author-detail-section-header">

              <div>

                <div className="author-page-eyebrow">
                  RESEARCH
                </div>

                <h2>
                  Research Papers
                </h2>

              </div>

              <span className="author-paper-count">
                {papers.length}{" "}
                {papers.length === 1
                  ? "paper"
                  : "papers"}
              </span>

            </div>


            {/* =================================================
                LOADING
                ================================================= */}

            {detailLoading && (
              <LoadingState />
            )}


            {/* =================================================
                ERROR
                ================================================= */}

            {!detailLoading &&
              detailError && (
                <ErrorState
                  message={detailError}
                />
              )}


            {/* =================================================
                EMPTY
                ================================================= */}

            {!detailLoading &&
              !detailError &&
              papers.length === 0 && (
                <div className="author-empty">

                  <div className="author-empty-icon">
                    📄
                  </div>

                  <h2>
                    No Research Papers
                  </h2>

                  <p>
                    No research papers are
                    currently associated
                    with this author.
                  </p>

                </div>
              )}


            {/* =================================================
                PAPER GRID
                ================================================= */}

            {!detailLoading &&
              !detailError &&
              papers.length > 0 && (
                <div className="author-paper-grid">

                  {papers.map(
                    (paper) => (
                      <button
                        type="button"
                        key={
                          paper.paper_id
                        }
                        className="author-paper-card"
                        onClick={() =>
                          navigate(
                            `/papers/${paper.paper_id}`,
                          )
                        }
                      >

                        <div className="author-paper-card-top">

                          <span className="author-paper-icon">
                            📄
                          </span>

                          <span className="author-paper-id">
                            PAPER #
                            {paper.paper_id}
                          </span>

                        </div>


                        <h3>
                          {paper.paper_name}
                        </h3>


                        <div className="author-paper-meta">

                          {paper.publication_year !==
                            null &&
                            paper.publication_year !==
                              undefined && (
                              <span>
                                📅{" "}
                                {
                                  paper.publication_year
                                }
                              </span>
                            )}

                          <span>
                            📚{" "}
                            {
                              paper.cited_by_count ??
                              0
                            }{" "}
                            citations
                          </span>

                        </div>


                        <div className="author-paper-footer">
                          View paper →
                        </div>

                      </button>
                    ),
                  )}

                </div>
              )}

          </section>

        </div>

      </main>
    );
  }


  /*
   * ==========================================================
   * AUTHORS SEARCH VIEW
   * ==========================================================
   */

  return (
    <main className="author-page">

      <div className="author-page-container">

        {/* ====================================================
            PAGE HEADER
            ==================================================== */}

        <section className="author-page-header">

          <div className="author-page-eyebrow">
            RESEARCHER DISCOVERY
          </div>

          <h1>
            Authors
          </h1>

          <p>
            Explore Researchers &amp; Their Work.
            <br />
            Find researchers by author name or ID
            and explore their research papers.
          </p>

        </section>


        {/* ====================================================
            SEARCH
            ==================================================== */}

        <section className="author-search-card">

          <div className="author-search-header">

            <span className="author-search-label">
              AUTHOR SEARCH
            </span>

            <h2>
              Find Researchers
            </h2>

          </div>


          <div className="author-search-form">

            <div className="author-search-input-wrapper">

              <span
                className="author-search-icon"
                aria-hidden="true"
              >
                👤
              </span>

              <input
                type="search"
                className="author-search-input"
                value={search}
                onChange={(event) =>
                  setSearch(
                    event.currentTarget.value,
                  )
                }
                onKeyDown={handleKeyDown}
                placeholder="Search by author name or ID..."
                aria-label="Search by author name or ID"
              />

            </div>


            <button
              type="button"
              className="author-search-button"
              disabled={
                loading ||
                search.trim().length === 0
              }
              onClick={handleSearch}
            >
              {loading
                ? "Searching..."
                : "Search"}
            </button>

          </div>

        </section>


        {/* ====================================================
            LOADING
            ==================================================== */}

        {loading && (
          <div className="author-loading">
            <LoadingState />
          </div>
        )}


        {/* ====================================================
            ERROR
            ==================================================== */}

        {!loading && error && (
          <div className="author-error">
            <ErrorState
              message={error}
            />
          </div>
        )}


        {/* ====================================================
            SEARCH RESULTS
            ==================================================== */}

        {!loading &&
          !error &&
          authors.length > 0 && (
            <section className="author-results">

              <div className="author-results-header">

                <div>

                  <div className="author-page-eyebrow">
                    SEARCH RESULTS
                  </div>

                  <h2 className="author-results-title">
                    {total.toLocaleString()}{" "}
                    {total === 1
                      ? "author"
                      : "authors"}{" "}
                    found
                  </h2>

                </div>


                <button
                  type="button"
                  className="author-clear-button"
                  onClick={handleClear}
                >
                  Clear Search
                </button>

              </div>


              {/* ==============================================
                  AUTHOR RESULT GRID
                  ============================================== */}

              <div className="author-grid">

                {authors.map(
                  (author) => (
                    <button
                      type="button"
                      key={
                        author.author_id
                      }
                      className="author-card"
                      onClick={() =>
                        handleAuthorClick(
                          author.author_id,
                        )
                      }
                    >

                      {/* ========================================
                          CARD TOP
                          ======================================== */}

                      <div className="author-card-top">

                        <div className="author-avatar">
                          {getInitials(
                            author.author_name,
                          )}
                        </div>

                        <span
                          className="author-arrow"
                          aria-hidden="true"
                        >
                          →
                        </span>

                      </div>


                      {/* ========================================
                          AUTHOR INFORMATION
                          ======================================== */}

                      <span className="author-card-label">
                        RESEARCHER
                      </span>

                      <h3 className="author-card-name">
                        {author.author_name}
                      </h3>


                      <div className="author-card-meta">

                        <span>
                          Author ID
                        </span>

                        <strong>
                          {author.author_id}
                        </strong>

                      </div>


                      {author.orcid && (
                        <div className="author-card-orcid">
                          ORCID{" "}
                          {author.orcid}
                        </div>
                      )}


                      {/* ========================================
                          CARD FOOTER
                          ======================================== */}

                      <div className="author-card-footer">
                        View research papers →
                      </div>

                    </button>
                  ),
                )}

              </div>


              {/* ==============================================
                  PAGINATION
                  ============================================== */}

              {totalPages > 1 && (
                <div className="author-pagination">

                  <button
                    type="button"
                    className="author-pagination-button"
                    disabled={page <= 1}
                    onClick={() =>
                      void searchAuthors(
                        search.trim(),
                        page - 1,
                      )
                    }
                  >
                    ← Previous
                  </button>


                  <span className="author-pagination-info">
                    Page {page} of {totalPages}
                  </span>


                  <button
                    type="button"
                    className="author-pagination-button"
                    disabled={
                      page >= totalPages
                    }
                    onClick={() =>
                      void searchAuthors(
                        search.trim(),
                        page + 1,
                      )
                    }
                  >
                    Next →
                  </button>

                </div>
              )}

            </section>
          )}


        {/* ====================================================
            NO RESULTS
            ==================================================== */}

        {!loading &&
          !error &&
          hasSearched &&
          authors.length === 0 && (
            <div className="author-empty">

              <div className="author-empty-icon">
                🔍
              </div>

              <h2>
                No Researchers Found
              </h2>

              <p>
                No authors matched{" "}
                <strong>
                  "{search}"
                </strong>
                . Try a different author
                name or ID.
              </p>

            </div>
          )}


        {/* ====================================================
            INITIAL STATE
            ==================================================== */}

        {!loading &&
          !error &&
          !hasSearched && (
            <div className="author-empty">

              <div className="author-empty-icon">
                👤
              </div>

              <h2>
                Find a Researcher
              </h2>

              <p>
                Enter an author's name or
                author ID above to discover
                their research papers.
              </p>

            </div>
          )}

      </div>

    </main>
  );
}

export default AuthorsPage;