import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { getPaperById } from "../api/paperApi";
import { getSimilarPapers } from "../api/recommendationApi";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import PaperCard from "../components/papers/PaperCard";

import type { PaperDetail } from "../types/paper";

function PaperDetailPage() {
  const { paperId } = useParams<{ paperId: string }>();
  const navigate = useNavigate();

  const [paper, setPaper] =
    useState<PaperDetail | null>(null);

  const [similarPapers, setSimilarPapers] =
    useState<PaperDetail[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [similarLoading, setSimilarLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    if (!paperId) {
      setError("Paper ID is missing.");
      setLoading(false);
      setSimilarLoading(false);
      return;
    }

    const id = Number(paperId);

    if (!Number.isInteger(id) || id <= 0) {
      setError("Invalid paper ID.");
      setLoading(false);
      setSimilarLoading(false);
      return;
    }

    let cancelled = false;

    const loadPaper = async (): Promise<void> => {
      try {
        setLoading(true);
        setError(null);

        const response =
          await getPaperById(id);

        if (!cancelled) {
          setPaper(response);
        }
      } catch (err) {
        console.error(
          "Failed to load paper:",
          err,
        );

        if (!cancelled) {
          setError(
            "Unable to load the paper.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    const loadSimilarPapers =
      async (): Promise<void> => {
        try {
          setSimilarLoading(true);

          const response =
            await getSimilarPapers(id, 5);

          if (!cancelled) {
            setSimilarPapers(
              response ?? [],
            );
          }
        } catch (err) {
          console.error(
            "Failed to load similar papers:",
            err,
          );

          if (!cancelled) {
            setSimilarPapers([]);
          }
        } finally {
          if (!cancelled) {
            setSimilarLoading(false);
          }
        }
      };

    void loadPaper();
    void loadSimilarPapers();

    return () => {
      cancelled = true;
    };
  }, [paperId]);

  // ==========================================================
  // Loading
  // ==========================================================

  if (loading) {
    return <LoadingState />;
  }

  // ==========================================================
  // Error
  // ==========================================================

  if (error) {
    return (
      <ErrorState
        message={error}
      />
    );
  }

  // ==========================================================
  // Missing paper
  // ==========================================================

  if (!paper) {
    return (
      <ErrorState
        message="Paper could not be found."
      />
    );
  }

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <main className="paper-detail-page">

      <div className="page-container">

        {/* ==================================================
            Back
            ================================================== */}

        <Link
          to="/search"
          className="back-link"
        >
          ← Back to Search
        </Link>


        {/* ==================================================
            Paper
            ================================================== */}

        <article className="paper-detail">

          {/* ------------------------------------------------
              Header
              ------------------------------------------------ */}

          <header className="paper-detail-header">

            <h1>
              {paper.paper_name}
            </h1>

            <div className="paper-detail-meta">

              {paper.publication_year && (
                <span>
                  Year:{" "}
                  {paper.publication_year}
                </span>
              )}

              <span>
                Citations:{" "}
                {paper.cited_by_count ?? 0}
              </span>

            </div>

          </header>


          {/* ------------------------------------------------
              Abstract
              ------------------------------------------------ */}

          <section className="paper-section">

            <h2>
              Abstract
            </h2>

            {paper.abstract ? (
              <p>
                {paper.abstract}
              </p>
            ) : (
              <p>
                No abstract available.
              </p>
            )}

          </section>


          {/* ------------------------------------------------
              Authors
              ------------------------------------------------ */}

          <section className="paper-section">

            <h2>
              Authors
            </h2>

            {paper.authors &&
            paper.authors.length > 0 ? (
              <ul className="paper-author-list">

                {paper.authors.map(
                  (author) => (
                    <li
                      key={
                        author.author_id
                      }
                    >
                      {author.author_name}
                    </li>
                  ),
                )}

              </ul>
            ) : (
              <p>
                No authors available.
              </p>
            )}

          </section>


          {/* ------------------------------------------------
              Topics
              ------------------------------------------------ */}

          <section className="paper-section">

            <h2>
              Topics
            </h2>

            {paper.topics &&
            paper.topics.length > 0 ? (
              <div className="topic-list">

                {paper.topics.map(
                  (topic) => (
                    <span
                      key={
                        topic.topic_id
                      }
                      className="topic-tag"
                    >
                      {
                        topic.topic_name
                      }
                    </span>
                  ),
                )}

              </div>
            ) : (
              <p>
                No topics available.
              </p>
            )}

          </section>


          {/* ------------------------------------------------
              DOI
              ------------------------------------------------ */}

          {paper.doi && (
            <section className="paper-section">

              <h2>
                DOI
              </h2>

              <a
                href={paper.doi}
                target="_blank"
                rel="noopener noreferrer"
              >
                {paper.doi}
              </a>

            </section>
          )}

        </article>


        {/* ==================================================
            Similar Papers
            ================================================== */}

        <section
          className="recommendation-section"
          aria-label="Similar papers"
        >

          <div className="recommendation-header">

            <div>
              <h2>
                Similar Papers
              </h2>

              <p>
                Papers with similar research
                content from this corpus.
              </p>
            </div>

          </div>


          {/* ------------------------------------------------
              Loading
              ------------------------------------------------ */}

          {similarLoading && (
            <LoadingState
              message="Finding similar papers..."
            />
          )}


          {/* ------------------------------------------------
              Results
              ------------------------------------------------ */}

          {!similarLoading &&
          similarPapers.length > 0 && (
            <div className="paper-grid">

              {similarPapers.map(
                (similarPaper) => (
                  <PaperCard
                    key={
                      similarPaper.paper_id
                    }
                    paper={similarPaper}
                    onClick={() =>
                      navigate(
                        `/papers/${similarPaper.paper_id}`,
                      )
                    }
                  />
                ),
              )}

            </div>
          )}


          {/* ------------------------------------------------
              Empty
              ------------------------------------------------ */}

          {!similarLoading &&
          similarPapers.length === 0 && (
            <p>
              No similar papers found.
            </p>
          )}

        </section>

      </div>

    </main>
  );
}

export default PaperDetailPage;