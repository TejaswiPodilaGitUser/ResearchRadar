import {
  useState,
} from "react";

import {
  useNavigate,
} from "react-router-dom";

import "../styles/entity-page.css";

import {
  getTopics,
} from "../api/topicApi";

import type {
  Topic,
} from "../types/topic";

import TopicCard from "../components/topics/TopicCard";

// ============================================================
// Topics Page
// ============================================================

function TopicsPage() {
  const navigate = useNavigate();

  const [
    search,
    setSearch,
  ] = useState("");

  const [
    topics,
    setTopics,
  ] = useState<Topic[]>([]);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    searched,
    setSearched,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  // ==========================================================
  // Search Topics
  // ==========================================================

  const handleSearch = async (): Promise<void> => {
    const keyword = search.trim();

    if (!keyword) {
      setTopics([]);
      setError(null);
      setSearched(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSearched(true);

      const response = await getTopics({
        keyword,
        page: 1,
        size: 20,
      });

      setTopics(response.results);
    } catch (err) {
      console.error(
        "Failed to search topics:",
        err,
      );

      setTopics([]);
      setError(
        "Unable to search topics.",
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // Search On Enter
  // ==========================================================

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>,
  ): void => {
    if (event.key === "Enter") {
      void handleSearch();
    }
  };

  // ==========================================================
  // Clear Search
  // ==========================================================

  const handleClear = (): void => {
    setSearch("");
    setTopics([]);
    setError(null);
    setSearched(false);
  };

  // ==========================================================
  // View Topic
  // ==========================================================

  const handleTopicClick = (
    topicId: number,
  ): void => {
    navigate(`/topics/${topicId}`);
  };

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <main className="entity-page">

      {/* ====================================================
          Hero
          ==================================================== */}

      <section className="entity-hero">

        <div className="entity-eyebrow">
          RESEARCH AREAS
        </div>

        <h1>
          Topics
        </h1>

        <p>
          Discover research areas, subjects,
          and emerging topics.
        </p>

      </section>

      {/* ====================================================
          Content
          ==================================================== */}

      <section className="entity-content">

        {/* ==================================================
            Search
            ================================================== */}

        <div className="entity-search">

          <span aria-hidden="true">
            🏷
          </span>

          <input
            type="search"
            value={search}
            onChange={(event) =>
              setSearch(
                event.target.value,
              )
            }
            onKeyDown={handleKeyDown}
            placeholder="Search by topic name, ID, or multiple values..."
            aria-label="Search topics"
          />

          <button
            type="button"
            onClick={() =>
              void handleSearch()
            }
            disabled={
              loading ||
              !search.trim()
            }
            className="entity-search-button"
          >
            {loading
              ? "Searching..."
              : "Search"}
          </button>

          {searched && !loading && (
            <button
              type="button"
              onClick={handleClear}
              className="entity-clear-button"
            >
              Clear
            </button>
          )}

        </div>

        {/* ==================================================
            Loading
            ================================================== */}

        {loading && (
          <div className="entity-empty">

            <div className="entity-empty-icon">
              🔎
            </div>

            <h2>
              Searching Topics
            </h2>

            <p>
              Finding matching research topics...
            </p>

          </div>
        )}

        {/* ==================================================
            Error
            ================================================== */}

        {!loading && error && (
          <div className="entity-empty">

            <div className="entity-empty-icon">
              ⚠️
            </div>

            <h2>
              Something went wrong
            </h2>

            <p>
              {error}
            </p>

          </div>
        )}

        {/* ==================================================
            Initial State
            ================================================== */}

        {!loading &&
          !error &&
          !searched && (
            <div className="entity-empty">

              <div className="entity-empty-icon">
                🏷
              </div>

              <h2>
                Explore Topics
              </h2>

              <p>
                Search by topic name or topic ID
                to discover related research papers.
              </p>

            </div>
          )}

        {/* ==================================================
            No Results
            ================================================== */}

        {!loading &&
          !error &&
          searched &&
          topics.length === 0 && (
            <div className="entity-empty">

              <div className="entity-empty-icon">
                🔎
              </div>

              <h2>
                No Topics Found
              </h2>

              <p>
                No topics matched your search.
              </p>

            </div>
          )}

        {/* ==================================================
            Results
            ================================================== */}

        {!loading &&
          !error &&
          topics.length > 0 && (
            <section className="entity-results">

              <div className="entity-results-header">

                <div>

                  <h2>
                    Topics
                  </h2>

                  <span>
                    {topics.length.toLocaleString()}
                    {" "}
                    {topics.length === 1
                      ? "topic"
                      : "topics"}
                    {" "}
                    found
                  </span>

                </div>

              </div>

              {/* ==================================================
                  Topic Cards
                  ================================================== */}

              <div className="entity-grid">

                {topics.map(
                  (topic) => (
                    <TopicCard
                      key={topic.topic_id}
                      topic={topic}
                      onClick={handleTopicClick}
                    />
                  ),
                )}

              </div>

            </section>
          )}

      </section>

    </main>
  );
}

export default TopicsPage;
