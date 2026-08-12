import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getPaperById } from "../api/paperApi";
import { getSimilarPapers } from "../api/recommendationApi";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import PaperCard from "../components/papers/PaperCard";

import type { PaperDetail } from "../types/paper";

function PaperDetailPage() {
  const { paperId } = useParams<{ paperId: string }>();

  const [paper, setPaper] = useState<PaperDetail | null>(null);
  const [similarPapers, setSimilarPapers] = useState<PaperDetail[]>([]);

  const [loading, setLoading] = useState(true);
  const [similarLoading, setSimilarLoading] = useState(true);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!paperId) {
      setError("Paper ID is missing.");
      setLoading(false);
      return;
    }

    const id = Number(paperId);

    if (!Number.isInteger(id) || id <= 0) {
      setError("Invalid paper ID.");
      setLoading(false);
      return;
    }

    const loadPaper = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await getPaperById(id);

        setPaper(response);
      } catch (err) {
        console.error("Failed to load paper:", err);
        setError("Unable to load the paper.");
      } finally {
        setLoading(false);
      }
    };

    const loadSimilarPapers = async () => {
      try {
        setSimilarLoading(true);

        const response = await getSimilarPapers(id, 5);

        setSimilarPapers(response);
      } catch (err) {
        console.error(
          "Failed to load similar papers:",
          err
        );

        setSimilarPapers([]);
      } finally {
        setSimilarLoading(false);
      }
    };

    void loadPaper();
    void loadSimilarPapers();
  }, [paperId]);

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  if (!paper) {
    return (
      <ErrorState message="Paper could not be found." />
    );
  }

  return (
    <main className="paper-detail-page">
      <div className="page-container">

        <Link
          to="/search"
          className="back-link"
        >
          ← Back to Search
        </Link>

        <article className="paper-detail">

          <header className="paper-detail-header">

            <h1>{paper.paper_name}</h1>

            <div className="paper-detail-meta">

              {paper.publication_year && (
                <span>
                  Year: {paper.publication_year}
                </span>
              )}

              {paper.cited_by_count !== null &&
                paper.cited_by_count !== undefined && (
                  <span>
                    Citations: {paper.cited_by_count}
                  </span>
                )}

            </div>

          </header>

          {paper.abstract && (
            <section className="paper-section">

              <h2>Abstract</h2>

              <p>
                {paper.abstract}
              </p>

            </section>
          )}

          <section className="paper-section">

            <h2>Authors</h2>

            {paper.authors && paper.authors.length > 0 ? (
              <ul className="paper-author-list">

                {paper.authors.map((author) => (
                  <li key={author.author_id}>
                    {author.author_name}
                  </li>
                ))}

              </ul>
            ) : (
              <p>No authors available.</p>
            )}

          </section>

          <section className="paper-section">

            <h2>Topics</h2>

            {paper.topics && paper.topics.length > 0 ? (
              <div className="topic-list">

                {paper.topics.map((topic) => (
                  <span
                    key={topic.topic_id}
                    className="topic-tag"
                  >
                    {topic.topic_name}
                  </span>
                ))}

              </div>
            ) : (
              <p>No topics available.</p>
            )}

          </section>

          {paper.doi && (
            <section className="paper-section">

              <h2>DOI</h2>

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

        <section className="recommendation-section">

          <h2>Similar Papers</h2>

          {similarLoading && (
            <LoadingState />
          )}

          {!similarLoading && similarPapers.length > 0 && (
            <div className="paper-grid">

              {similarPapers.map((similarPaper) => (
                <PaperCard
                  key={similarPaper.paper_id}
                  paper={similarPaper}
                />
              ))}

            </div>
          )}

          {!similarLoading && similarPapers.length === 0 && (
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