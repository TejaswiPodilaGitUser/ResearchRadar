import {
  useEffect,
  useState,
} from "react";

import {
  Link,
  useParams,
} from "react-router-dom";

import {
  getTopicById,
} from "../api/topicApi";

import type {
  TopicDetail,
  TopicPaper,
} from "../types/topic";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";

import "../styles/entity-page.css";
import "../styles/topic-page.css";

// ============================================================
// Topic Detail Page
// ============================================================

function TopicDetailPage() {
  const {
    topicId,
  } = useParams<{
    topicId: string;
  }>();

  const [
    topic,
    setTopic,
  ] = useState<TopicDetail | null>(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  // ==========================================================
  // Load Topic
  // ==========================================================

  useEffect(() => {
    let cancelled = false;

    const loadTopic = async (): Promise<void> => {
      if (!topicId) {
        setError("Topic ID is missing.");
        setLoading(false);
        return;
      }

      const id = Number(topicId);

      if (
        !Number.isInteger(id) ||
        id <= 0
      ) {
        setError("Invalid topic ID.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const response =
          await getTopicById(id);

        if (!cancelled) {
          setTopic(response);
        }
      } catch (err) {
        console.error(
          "Failed to load topic:",
          err,
        );

        if (!cancelled) {
          setTopic(null);
          setError(
            "Unable to load the topic.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void loadTopic();

    return () => {
      cancelled = true;
    };
  }, [topicId]);

  // ==========================================================
  // Loading
  // ==========================================================

  if (loading) {
    return (
      <main className="entity-page">
        <section className="entity-content">
          <LoadingState />
        </section>
      </main>
    );
  }

  // ==========================================================
  // Error
  // ==========================================================

  if (error) {
    return (
      <main className="entity-page">
        <section className="entity-content">

          <Link
            to="/topics"
            className="entity-back-link"
          >
            ← Back to Topics
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

        </section>
      </main>
    );
  }

  // ==========================================================
  // Topic Not Found
  // ==========================================================

  if (!topic) {
    return (
      <main className="entity-page">
        <section className="entity-content">

          <Link
            to="/topics"
            className="entity-back-link"
          >
            ← Back to Topics
          </Link>

          <div
            style={{
              marginTop: "24px",
            }}
          >
            <ErrorState
              message="Topic could not be found."
            />
          </div>

        </section>
      </main>
    );
  }

  // ==========================================================
  // Papers
  // ==========================================================

  const papers: TopicPaper[] =
    topic.papers ?? [];

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <main className="entity-page">

      <section className="entity-content">

        {/* ==================================================
            Back
            ================================================== */}

        <Link
          to="/topics"
          className="entity-back-link"
        >
          ← Back to Topics
        </Link>

        {/* ==================================================
            Topic Header
            ================================================== */}

        <article className="entity-detail">

          <div className="entity-detail-header">

            <div className="entity-detail-icon">
              🏷
            </div>

            <div>

              <div className="entity-eyebrow">
                RESEARCH AREA
              </div>

              <h1>
                {topic.topic_name}
              </h1>

              <p className="entity-detail-meta">
                Topic ID:{" "}
                <strong>
                  {topic.topic_id}
                </strong>
              </p>

            </div>

          </div>

        </article>

        {/* ==================================================
            Research Papers
            ================================================== */}

        <section className="entity-results">

          <div className="entity-results-header">

            <div>

              <div className="entity-eyebrow">
                RESEARCH
              </div>

              <h2>
                Research Papers
              </h2>

              <p>
                Papers associated with this
                research topic.
              </p>

            </div>

            <span>
              {papers.length.toLocaleString()}{" "}
              {papers.length === 1
                ? "paper"
                : "papers"}
            </span>

          </div>

          {/* ==================================================
              No Papers
              ================================================== */}

          {papers.length === 0 && (
            <div className="entity-empty">

              <div className="entity-empty-icon">
                📄
              </div>

              <h2>
                No Research Papers
              </h2>

              <p>
                No papers are currently
                associated with this topic.
              </p>

            </div>
          )}

          {/* ==================================================
              Papers
              ================================================== */}

          {papers.length > 0 && (
            <div className="entity-grid">

              {papers.map(
                (paper) => (
                  <article
                    key={paper.paper_id}
                    className="entity-card"
                  >

                    {/* Paper ID */}

                    <div className="entity-card-header">

                      <span className="entity-card-id">
                        Paper ID:{" "}
                        {paper.paper_id}
                      </span>

                    </div>

                    {/* Paper Name */}

                    <h3 className="entity-card-title">
                      {paper.paper_name}
                    </h3>

                    {/* Metadata */}

                    <div className="entity-card-meta">

                      {paper.publication_year !==
                        null && (
                        <span>
                          Published:{" "}
                          {paper.publication_year}
                        </span>
                      )}

                      {paper.cited_by_count !==
                        null && (
                        <span>
                          Citations:{" "}
                          {paper.cited_by_count}
                        </span>
                      )}

                    </div>

                    {/* View Paper */}

                    <Link
                      to={`/papers/${paper.paper_id}`}
                      className="entity-card-action"
                    >
                      <span>
                        View Paper
                      </span>

                      <span
                        aria-hidden="true"
                      >
                        →
                      </span>
                    </Link>

                  </article>
                ),
              )}

            </div>
          )}

        </section>

      </section>

    </main>
  );
}

export default TopicDetailPage;