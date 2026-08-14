import {
  useState,
  type KeyboardEvent,
} from "react";

import { useNavigate } from "react-router-dom";

import { useAuthors } from "../hooks/useAuthors";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";

import "../styles/entity-page.css";

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
      part
        .charAt(0)
        .toUpperCase(),
    )
    .join("");
}

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

  const handleAuthorClick = (
    authorId: number,
  ): void => {
    void loadAuthor(authorId);
  };

  const handleBack = (): void => {
    clearSelectedAuthor();
  };

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
      <main className="entity-page">

        <section className="entity-hero">

          <div className="entity-eyebrow">
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

        <section className="entity-content">

          <button
            type="button"
            className="secondary-button"
            onClick={handleBack}
          >
            ← Back to Authors
          </button>

          <section
            style={{
              marginTop: "24px",
              padding: "28px",
              background: "#ffffff",
              border:
                "1px solid #e5e7eb",
              borderRadius: "16px",
              display: "flex",
              alignItems: "center",
              gap: "20px",
            }}
          >

            <div
              style={{
                width: "64px",
                height: "64px",
                minWidth: "64px",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "#f1f5f9",
                color: "#334155",
                fontSize: "20px",
                fontWeight: 700,
              }}
            >
              {getInitials(
                selectedAuthor.author_name,
              )}
            </div>

            <div>

              <div className="entity-eyebrow">
                RESEARCHER
              </div>

              <h2
                style={{
                  margin:
                    "4px 0 10px",
                  fontSize: "26px",
                }}
              >
                {selectedAuthor.author_name}
              </h2>

              <div
                style={{
                  display: "flex",
                  gap: "20px",
                  flexWrap: "wrap",
                  color: "#6b7280",
                  fontSize: "14px",
                }}
              >

                <span>
                  Author ID:{" "}
                  <strong>
                    {
                      selectedAuthor.author_id
                    }
                  </strong>
                </span>

                {selectedAuthor.orcid && (
                  <span>
                    ORCID:{" "}
                    <strong>
                      {
                        selectedAuthor.orcid
                      }
                    </strong>
                  </span>
                )}

              </div>

            </div>

          </section>

          <section
            style={{
              marginTop: "36px",
            }}
          >

            <div
              style={{
                display: "flex",
                alignItems: "flex-end",
                justifyContent:
                  "space-between",
                gap: "20px",
                marginBottom: "20px",
              }}
            >

              <div>

                <div className="entity-eyebrow">
                  RESEARCH
                </div>

                <h2
                  style={{
                    margin: 0,
                    fontSize: "26px",
                  }}
                >
                  Research Papers
                </h2>

              </div>

              <span
                style={{
                  padding:
                    "7px 12px",
                  borderRadius: "20px",
                  background:
                    "#f1f5f9",
                  color: "#475569",
                  fontSize: "13px",
                  fontWeight: 600,
                  whiteSpace:
                    "nowrap",
                }}
              >
                {papers.length}{" "}
                {papers.length === 1
                  ? "paper"
                  : "papers"}
              </span>

            </div>

            {detailLoading && (
              <LoadingState />
            )}

            {!detailLoading &&
              detailError && (
                <ErrorState
                  message={
                    detailError
                  }
                />
              )}

            {!detailLoading &&
              !detailError &&
              papers.length === 0 && (
                <div className="entity-empty">

                  <div className="entity-empty-icon">
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

            {!detailLoading &&
              !detailError &&
              papers.length > 0 && (
                <div className="recommendation-grid">

                  {papers.map(
                    (paper) => (
                      <button
                        type="button"
                        key={
                          paper.paper_id
                        }
                        className="paper-result-card"
                        onClick={() =>
                          navigate(
                            `/papers/${paper.paper_id}`,
                          )
                        }
                        style={{
                          padding:
                            "24px",
                          cursor:
                            "pointer",
                        }}
                      >

                        <div
                          style={{
                            display:
                              "flex",
                            justifyContent:
                              "space-between",
                            alignItems:
                              "center",
                            marginBottom:
                              "18px",
                          }}
                        >

                          <span
                            style={{
                              fontSize:
                                "24px",
                            }}
                          >
                            📄
                          </span>

                          <span
                            style={{
                              color:
                                "#9ca3af",
                              fontSize:
                                "12px",
                              fontWeight:
                                600,
                            }}
                          >
                            PAPER #
                            {
                              paper.paper_id
                            }
                          </span>

                        </div>

                        <h3
                          style={{
                            margin:
                              "0 0 18px",
                            fontSize:
                              "17px",
                            lineHeight:
                              1.45,
                          }}
                        >
                          {
                            paper.paper_name
                          }
                        </h3>

                        <div
                          style={{
                            display:
                              "flex",
                            flexWrap:
                              "wrap",
                            gap: "14px",
                            color:
                              "#6b7280",
                            fontSize:
                              "13px",
                          }}
                        >

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

                        <div
                          style={{
                            marginTop:
                              "22px",
                            color:
                              "#2563eb",
                            fontSize:
                              "13px",
                            fontWeight:
                              600,
                          }}
                        >
                          View paper →
                        </div>

                      </button>
                    ),
                  )}

                </div>
              )}

          </section>

        </section>

      </main>
    );
  }

  /*
   * ==========================================================
   * AUTHORS SEARCH VIEW
   * ==========================================================
   */

  return (
    <main className="entity-page">

      <section className="entity-hero">

        <div className="entity-eyebrow">
          RESEARCHER DISCOVERY
        </div>

        <h1>
          Authors
        </h1>

        <p>
          Explore Researchers & Their Work.<br></br>
          Find researchers by author name or ID and explore their research papers.
        </p>

      </section>

      <section className="entity-content">

        <section
          style={{
            background:
              "#ffffff",
            border:
              "1px solid #e5e7eb",
            borderRadius:
              "16px",
            padding: "24px",
          }}
        >

          <div
            style={{
              marginBottom:
                "18px",
            }}
          >

            <div className="entity-eyebrow">
              AUTHOR SEARCH
            </div>

            <h2
              style={{
                margin: 0,
                fontSize: "22px",
              }}
            >
              Find Researchers
            </h2>

          </div>

          <div
            style={{
              display: "flex",
              gap: "12px",
            }}
          >

            <div
              className="entity-search"
              style={{
                flex: 1,
              }}
            >

              <span aria-hidden="true">
                👤
              </span>

              <input
                type="search"
                value={search}
                onChange={(event) =>
                  setSearch(
                    event
                      .currentTarget
                      .value,
                  )
                }
                onKeyDown={
                  handleKeyDown
                }
                placeholder="Search by author name or ID..."
                aria-label="Search by author name or ID"
              />

            </div>

            <button
              type="button"
              className="primary-button"
              disabled={
                loading ||
                search.trim()
                  .length === 0
              }
              onClick={
                handleSearch
              }
            >
              {loading
                ? "Searching..."
                : "Search"}
            </button>

          </div>

        </section>

        {loading && (
          <div
            style={{
              marginTop:
                "24px",
            }}
          >
            <LoadingState />
          </div>
        )}

        {!loading && error && (
          <div
            style={{
              marginTop:
                "20px",
            }}
          >
            <ErrorState
              message={error}
            />
          </div>
        )}

        {/*
         * ======================================================
         * RESULTS
         * ======================================================
         */}

        {!loading &&
          !error &&
          authors.length > 0 && (
            <section
              style={{
                marginTop:
                  "32px",
              }}
            >

              <div
                style={{
                  display:
                    "flex",
                  alignItems:
                    "flex-end",
                  justifyContent:
                    "space-between",
                  gap: "20px",
                  marginBottom:
                    "20px",
                }}
              >

                <div>

                  <div className="entity-eyebrow">
                    SEARCH RESULTS
                  </div>

                  <h2
                    style={{
                      margin: 0,
                      fontSize:
                        "24px",
                    }}
                  >
                    {
                      total.toLocaleString()
                    }{" "}
                    {
                      total === 1
                        ? "author"
                        : "authors"
                    }{" "}
                    found
                  </h2>

                </div>

                <button
                  type="button"
                  className="secondary-button"
                  onClick={
                    handleClear
                  }
                >
                  Clear Search
                </button>

              </div>

              <div className="recommendation-grid">

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
                      style={{
                        padding:
                          "24px",
                        cursor:
                          "pointer",
                      }}
                    >

                      <div
                        style={{
                          display:
                            "flex",
                          alignItems:
                            "center",
                          justifyContent:
                            "space-between",
                          marginBottom:
                            "18px",
                        }}
                      >

                        <div
                          style={{
                            width:
                              "52px",
                            height:
                              "52px",
                            borderRadius:
                              "50%",
                            display:
                              "flex",
                            alignItems:
                              "center",
                            justifyContent:
                              "center",
                            background:
                              "#f1f5f9",
                            color:
                              "#334155",
                            fontWeight:
                              700,
                            fontSize:
                              "16px",
                          }}
                        >
                          {getInitials(
                            author.author_name,
                          )}
                        </div>

                        <span
                          aria-hidden="true"
                          style={{
                            color:
                              "#94a3b8",
                            fontSize:
                              "20px",
                          }}
                        >
                          →
                        </span>

                      </div>

                      <div className="entity-eyebrow">
                        RESEARCHER
                      </div>

                      <h3
                        style={{
                          margin:
                            "6px 0 14px",
                          fontSize:
                            "18px",
                        }}
                      >
                        {
                          author.author_name
                        }
                      </h3>

                      <div
                        style={{
                          display:
                            "flex",
                          alignItems:
                            "center",
                          gap: "8px",
                          color:
                            "#6b7280",
                          fontSize:
                            "13px",
                        }}
                      >

                        <span>
                          Author ID
                        </span>

                        <strong>
                          {
                            author.author_id
                          }
                        </strong>

                      </div>

                      {author.orcid && (
                        <div
                          style={{
                            marginTop:
                              "8px",
                            color:
                              "#6b7280",
                            fontSize:
                              "12px",
                          }}
                        >
                          ORCID{" "}
                          {
                            author.orcid
                          }
                        </div>
                      )}

                      <div
                        style={{
                          marginTop:
                            "22px",
                          paddingTop:
                            "16px",
                          borderTop:
                            "1px solid #f1f5f9",
                          color:
                            "#2563eb",
                          fontSize:
                            "13px",
                          fontWeight:
                            600,
                        }}
                      >
                        View research
                        papers →
                      </div>

                    </button>
                  ),
                )}

              </div>

              {totalPages > 1 && (
                <div
                  style={{
                    display:
                      "flex",
                    alignItems:
                      "center",
                    justifyContent:
                      "center",
                    gap: "20px",
                    marginTop:
                      "32px",
                  }}
                >

                  <button
                    type="button"
                    className="secondary-button"
                    disabled={
                      page <= 1
                    }
                    onClick={() =>
                      void searchAuthors(
                        search.trim(),
                        page - 1,
                      )
                    }
                  >
                    ← Previous
                  </button>

                  <span
                    style={{
                      color:
                        "#6b7280",
                      fontSize:
                        "14px",
                    }}
                  >
                    Page{" "}
                    {page}{" "}
                    of{" "}
                    {totalPages}
                  </span>

                  <button
                    type="button"
                    className="secondary-button"
                    disabled={
                      page >=
                      totalPages
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

        {/*
         * ======================================================
         * SEARCH COMPLETED BUT NO RESULTS
         * ======================================================
         */}

        {!loading &&
          !error &&
          hasSearched &&
          authors.length === 0 && (
            <div className="entity-empty">

              <div className="entity-empty-icon">
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
                . Try a different
                author name or ID.
              </p>

            </div>
          )}

        {/*
         * ======================================================
         * INITIAL STATE
         * ======================================================
         */}

        {!loading &&
          !error &&
          !hasSearched && (
            <div className="entity-empty">

              <div className="entity-empty-icon">
                👤
              </div>

              <h2>
                Find a Researcher
              </h2>

              <p>
                Enter an author's name
                or author ID above to
                discover their research
                papers.
              </p>

            </div>
          )}

      </section>

    </main>
  );
}

export default AuthorsPage;