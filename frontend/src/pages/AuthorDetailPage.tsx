import {
  useEffect,
  useState,
} from "react";

import {
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  getAuthorById,
  type AuthorDetail,
  type AuthorPaper,
} from "../api/authorApi";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";



// ============================================================
// Helpers
// ============================================================

function getInitials(name: string): string {
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

// ============================================================
// Author Detail Page
// ============================================================

function AuthorDetailPage() {
  const navigate = useNavigate();

  const {
    authorId,
  } = useParams<{
    authorId: string;
  }>();

  const [
    author,
    setAuthor,
  ] = useState<AuthorDetail | null>(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  // ==========================================================
  // Load Author
  // ==========================================================

  useEffect(() => {
    let cancelled = false;

    const loadAuthor = async (): Promise<void> => {
      if (!authorId) {
        if (!cancelled) {
          setError("Author ID is missing.");
          setLoading(false);
        }

        return;
      }

      const id = Number(authorId);

      if (
        !Number.isInteger(id) ||
        id <= 0
      ) {
        if (!cancelled) {
          setError("Invalid author ID.");
          setLoading(false);
        }

        return;
      }

      try {
        setLoading(true);
        setError(null);

        const response =
          await getAuthorById(id);

        if (!cancelled) {
          setAuthor(response);
        }
      } catch (err) {
        console.error(
          "Failed to load author:",
          err,
        );

        if (!cancelled) {
          setAuthor(null);
          setError(
            "Unable to load the author.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void loadAuthor();

    return () => {
      cancelled = true;
    };
  }, [authorId]);

  // ==========================================================
  // Loading
  // ==========================================================

  if (loading) {
    return (
      <main className="author-detail-page">
        <div className="author-page-container">
          <LoadingState />
        </div>
      </main>
    );
  }

  // ==========================================================
  // Error
  // ==========================================================

  if (error) {
    return (
      <main className="author-detail-page">
        <div className="author-page-container">

          <Link
            to="/authors"
            className="author-back-link"
          >
            ← Back to Authors
          </Link>

          <div
            style={{
              marginTop: "24px",
            }}
          >
            <ErrorState
              message={error}
            />
          </div>

        </div>
      </main>
    );
  }

  // ==========================================================
  // Author Not Found
  // ==========================================================

  if (!author) {
    return (
      <main className="author-detail-page">
        <div className="author-page-container">

          <Link
            to="/authors"
            className="author-back-link"
          >
            ← Back to Authors
          </Link>

          <div
            style={{
              marginTop: "24px",
            }}
          >
            <ErrorState
              message="Author could not be found."
            />
          </div>

        </div>
      </main>
    );
  }

  // ==========================================================
  // Papers
  // ==========================================================

  const papers: AuthorPaper[] =
    author.papers ?? [];

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <main className="author-detail-page">

      <div className="author-page-container">

        {/* ==================================================
            Back
            ================================================== */}

        <Link
          to="/authors"
          className="author-back-link"
        >
          ← Back to Authors
        </Link>

        {/* ==================================================
            Author Profile
            ================================================== */}

        <article className="author-profile">

          <header className="author-profile-header">

            <div className="author-profile-avatar">
              {getInitials(
                author.author_name,
              )}
            </div>

            <div className="author-profile-content">

              <span className="author-section-label">
                RESEARCHER
              </span>

              <h1>
                {author.author_name}
              </h1>

              <div className="author-profile-meta">

                <span>
                  Author ID:{" "}
                  <strong>
                    {author.author_id}
                  </strong>
                </span>

                {author.orcid && (
                  <span>
                    ORCID:{" "}
                    <strong>
                      {author.orcid}
                    </strong>
                  </span>
                )}

              </div>

            </div>

          </header>

        </article>

        {/* ==================================================
            Research Papers
            ================================================== */}

        <section className="author-papers-section">

          <header className="author-papers-header">

            <div>

              <span className="author-section-label">
                RESEARCH
              </span>

              <h2>
                Research Papers
              </h2>

              <p>
                Published research associated
                with this author.
              </p>

            </div>

            <span className="author-paper-count">
              {papers.length.toLocaleString()}{" "}
              {papers.length === 1
                ? "paper"
                : "papers"}
            </span>

          </header>

          {/* ==================================================
              No Papers
              ================================================== */}

          {papers.length === 0 && (
            <div className="author-no-papers">

              <div
                className="author-empty-icon"
                aria-hidden="true"
              >
                📄
              </div>

              <h3>
                No research papers found
              </h3>

              <p>
                No papers are currently
                associated with this author.
              </p>

            </div>
          )}

          {/* ==================================================
              Papers
              ================================================== */}

          {papers.length > 0 && (
            <div className="author-paper-grid">

              {papers.map(
                (
                  paper: AuthorPaper,
                ) => (
                  <button
                    type="button"
                    key={paper.paper_id}
                    className="author-paper-card"
                    onClick={() =>
                      navigate(
                        `/papers/${paper.paper_id}`,
                      )
                    }
                  >

                    {/* Paper Header */}

                    <div className="author-paper-top">

                      <span
                        className="author-paper-icon"
                        aria-hidden="true"
                      >
                        📄
                      </span>

                      <span className="author-paper-id">
                        Paper ID{" "}
                        {paper.paper_id}
                      </span>

                    </div>

                    {/* Paper Title */}

                    <h3>
                      {paper.paper_name}
                    </h3>

                    {/* Paper Metadata */}

                    <div className="author-paper-meta">

                      {paper.publication_year !==
                        null &&
                        paper.publication_year !==
                          undefined && (
                          <span>
                            Year{" "}
                            {paper.publication_year}
                          </span>
                        )}

                      <span>
                        {paper.cited_by_count ??
                          0}{" "}
                        citations
                      </span>

                    </div>

                    {/* Footer */}

                    <div className="author-paper-footer">

                      View paper{" "}

                      <span
                        aria-hidden="true"
                      >
                        →
                      </span>

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

export default AuthorDetailPage;

