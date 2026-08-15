import {
  useState,
} from "react";

import {
  Link,
} from "react-router-dom";

import "../styles/recommendations-page.css";

import {
  getTrendingPapers,
  getEmergingTopics,
  getPapersByTopic,
} from "../api/recommendationApi";

import type {
  RecommendationPaper,
  EmergingTopic,
} from "../types/recommendation";


// ============================================================
// Recommendation View
// ============================================================

type RecommendationView =
  | "home"
  | "trending"
  | "emerging"
  | "topic-papers";


// ============================================================
// Topic Papers Response
// ============================================================

type TopicPapersResponse = {
  topic_id: number;
  topic_name: string;
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  has_previous: boolean;
  has_next: boolean;
  results: RecommendationPaper[];
};


// ============================================================
// Page
// ============================================================

function RecommendationsPage() {

  const [view, setView] =
    useState<RecommendationView>("home");

  const [trendingPapers, setTrendingPapers] =
    useState<RecommendationPaper[]>([]);

  const [emergingTopics, setEmergingTopics] =
    useState<EmergingTopic[]>([]);

  const [topicPapers, setTopicPapers] =
    useState<RecommendationPaper[]>([]);

  const [selectedTopicId, setSelectedTopicId] =
    useState<number | null>(null);

  const [selectedTopicName, setSelectedTopicName] =
    useState<string>("");

  const [topicPage, setTopicPage] =
    useState(1);

  const [topicTotalPages, setTopicTotalPages] =
    useState(1);

  const [topicTotal, setTopicTotal] =
    useState(0);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  // ==========================================================
  // Load Trending Papers
  // ==========================================================

  async function handleTrending(): Promise<void> {

    setView("trending");

    setLoading(true);

    setError(null);

    try {

      const results =
        await getTrendingPapers(10);

      setTrendingPapers(results);

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load trending papers.",
      );

      setTrendingPapers([]);

    } finally {

      setLoading(false);

    }
  }


  // ==========================================================
  // Load Emerging Topics
  // ==========================================================

  async function handleEmergingTopics(): Promise<void> {

    setView("emerging");

    setLoading(true);

    setError(null);

    try {

      const results =
        await getEmergingTopics(10);

      setEmergingTopics(results);

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load emerging topics.",
      );

      setEmergingTopics([]);

    } finally {

      setLoading(false);

    }
  }


  // ==========================================================
  // Load Topic Papers
  // ==========================================================

  async function handleTopicPapers(
    topicId: number,
    topicName: string,
    page = 1,
  ): Promise<void> {

    setView("topic-papers");

    setLoading(true);

    setError(null);

    setSelectedTopicId(topicId);

    setSelectedTopicName(topicName);

    try {

      const response: TopicPapersResponse =
        await getPapersByTopic(
          topicId,
          page,
          10,
        );

      setTopicPapers(
        response.results,
      );

      setTopicPage(
        response.page,
      );

      setTopicTotalPages(
        response.total_pages,
      );

      setTopicTotal(
        response.total,
      );

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load papers for this topic.",
      );

      setTopicPapers([]);

    } finally {

      setLoading(false);

    }
  }


  // ==========================================================
  // Previous Topic Page
  // ==========================================================

  function handlePreviousTopicPage(): void {

    if (
      selectedTopicId === null ||
      topicPage <= 1 ||
      loading
    ) {
      return;
    }

    void handleTopicPapers(
      selectedTopicId,
      selectedTopicName,
      topicPage - 1,
    );
  }


  // ==========================================================
  // Next Topic Page
  // ==========================================================

  function handleNextTopicPage(): void {

    if (
      selectedTopicId === null ||
      topicPage >= topicTotalPages ||
      loading
    ) {
      return;
    }

    void handleTopicPapers(
      selectedTopicId,
      selectedTopicName,
      topicPage + 1,
    );
  }


  // ==========================================================
  // Back To Recommendations
  // ==========================================================

  function handleBack(): void {

    setView("home");

    setError(null);

    setLoading(false);

    setTopicPapers([]);

    setSelectedTopicId(null);

    setSelectedTopicName("");

    setTopicPage(1);

    setTopicTotalPages(1);

    setTopicTotal(0);
  }


  // ==========================================================
  // Back To Emerging Topics
  // ==========================================================

  function handleBackToEmergingTopics(): void {

    setView("emerging");

    setError(null);

    setLoading(false);

    setTopicPapers([]);

    setSelectedTopicId(null);

    setSelectedTopicName("");

    setTopicPage(1);

    setTopicTotalPages(1);

    setTopicTotal(0);
  }


  // ==========================================================
  // Home View
  // ==========================================================

  if (view === "home") {

    return (
      <main className="recommendations-page">

        <div className="recommendations-container">

          {/* ==================================================
              HERO
              ================================================== */}

          <section className="recommendations-hero">

            <div className="recommendations-eyebrow">
              DISCOVERY
            </div>

            <h1>
              Recommendations
            </h1>

            <p>
              Discover trending research, emerging topics,
              and papers related to your research interests.
            </p>

          </section>


          {/* ==================================================
              RECOMMENDATION GRID
              ================================================== */}

          <section className="recommendation-grid">

            {/* ==================================================
                TRENDING RESEARCH
                ================================================== */}

            <button
              type="button"
              className="recommendation-card"
              onClick={() => {
                void handleTrending();
              }}
            >

              <div className="recommendation-icon">
                🔥
              </div>

              <h2>
                Trending Research
              </h2>

              <p>
                Explore the top research papers
                gaining attention across the corpus.
              </p>

              <span className="recommendation-action">
                View Top 10 →
              </span>

            </button>


            {/* ==================================================
                EMERGING TOPICS
                ================================================== */}

            <button
              type="button"
              className="recommendation-card"
              onClick={() => {
                void handleEmergingTopics();
              }}
            >

              <div className="recommendation-icon">
                📈
              </div>

              <h2>
                Emerging Topics
              </h2>

              <p>
                Find research topics showing increasing
                activity and citation interest.
              </p>

              <span className="recommendation-action">
                View Top 10 →
              </span>

            </button>


            {/* ==================================================
                SIMILAR PAPERS
                ================================================== */}

            <Link
              to="/papers"
              className="recommendation-card"
            >

              <div className="recommendation-icon">
                ✦
              </div>

              <h2>
                Similar Papers
              </h2>

              <p>
                Explore papers that are semantically
                similar to a selected research paper.
              </p>

              <span className="recommendation-action">
                Open a Paper →
              </span>

            </Link>

          </section>

        </div>

      </main>
    );
  }


  // ==========================================================
  // Results View
  // ==========================================================

  return (
    <main className="recommendations-page">

      <div className="recommendations-container">

        {/* ====================================================
            HERO
            ==================================================== */}

        <section className="recommendations-hero">

          {/* ==================================================
              BACK BUTTON
              ================================================== */}

          <button
            type="button"
            className="recommendation-back"
            onClick={
              view === "topic-papers"
                ? handleBackToEmergingTopics
                : handleBack
            }
          >
            {view === "topic-papers"
              ? "← Emerging Topics"
              : "← Recommendations"}
          </button>


          <div className="recommendations-eyebrow">
            DISCOVERY
          </div>


          {/* ==================================================
              TITLE
              ================================================== */}

          <h1>

            {view === "trending" &&
              "Trending Research"}

            {view === "emerging" &&
              "Emerging Topics"}

            {view === "topic-papers" &&
              selectedTopicName}

          </h1>


          {/* ==================================================
              DESCRIPTION
              ================================================== */}

          <p>

            {view === "trending" &&
              "Top 10 research papers gaining attention across the corpus."}

            {view === "emerging" &&
              "Top 10 research topics showing increasing activity and citation interest."}

            {view === "topic-papers" &&
              `${topicTotal} papers associated with this topic.`}

          </p>

        </section>


        {/* ====================================================
            RESULTS
            ==================================================== */}

        <section className="recommendation-content">


          {/* ==================================================
              ERROR
              ================================================== */}

          {error && (

            <div className="recommendation-error">
              {error}
            </div>

          )}


          {/* ==================================================
              LOADING
              ================================================== */}

          {loading && (

            <div className="recommendation-loading">
              Loading recommendations...
            </div>

          )}


          {/* ==================================================
              TRENDING PAPERS
              ================================================== */}

          {!loading &&
            !error &&
            view === "trending" && (

              <div className="recommendation-results">

                {trendingPapers.map(
                  (paper, index) => (

                    <Link
                      key={paper.paper_id}
                      to={`/papers/${paper.paper_id}`}
                      className="recommendation-result"
                    >

                      <div className="recommendation-rank">
                        {index + 1}
                      </div>

                      <div className="recommendation-result-content">

                        <div className="recommendation-card-label">
                          PAPER ID
                        </div>

                        <div className="recommendation-card-id">
                          {paper.paper_id}
                        </div>

                        <h2>
                          {paper.paper_name}
                        </h2>

                        <div className="recommendation-card-meta">

                          <span>
                            Published{" "}
                            {paper.publication_year ?? "N/A"}
                          </span>

                          <span>
                            Citations:{" "}
                            {paper.cited_by_count ?? 0}
                          </span>

                        </div>

                      </div>

                    </Link>

                  ),
                )}

              </div>

          )}


          {/* ==================================================
              EMERGING TOPICS
              ================================================== */}

          {!loading &&
            !error &&
            view === "emerging" && (

              <div className="recommendation-results">

                {emergingTopics.map(
                  (topic, index) => (

                    <button
                      key={topic.topic_id}
                      type="button"
                      className="recommendation-result"
                      onClick={() => {
                        void handleTopicPapers(
                          topic.topic_id,
                          topic.topic_name,
                          1,
                        );
                      }}
                    >

                      <div className="recommendation-rank">
                        {index + 1}
                      </div>

                      <div className="recommendation-result-content">

                        <div className="recommendation-card-label">
                          TOPIC ID
                        </div>

                        <div className="recommendation-card-id">
                          {topic.topic_id}
                        </div>

                        <h2>
                          {topic.topic_name}
                        </h2>

                        <div className="recommendation-card-meta">

                          <span>
                            Papers:{" "}
                            {topic.paper_count}
                          </span>

                          <span>
                            Recent:{" "}
                            {topic.recent_paper_count}
                          </span>

                          <span>
                            Citations:{" "}
                            {topic.citation_count}
                          </span>

                        </div>

                        <div className="recommendation-topic-action">
                          View all papers →
                        </div>

                      </div>

                    </button>

                  ),
                )}

              </div>

          )}


          {/* ==================================================
              TOPIC PAPERS
              ================================================== */}

          {!loading &&
            !error &&
            view === "topic-papers" && (

              <>

                <div className="recommendation-results">

                  {topicPapers.map(
                    (paper, index) => (

                      <Link
                        key={paper.paper_id}
                        to={`/papers/${paper.paper_id}`}
                        className="recommendation-result"
                      >

                        <div className="recommendation-rank">
                          {(
                            (topicPage - 1) * 10
                          ) + index + 1}
                        </div>

                        <div className="recommendation-result-content">

                          <div className="recommendation-card-label">
                            PAPER ID
                          </div>

                          <div className="recommendation-card-id">
                            {paper.paper_id}
                          </div>

                          <h2>
                            {paper.paper_name}
                          </h2>

                          <div className="recommendation-card-meta">

                            <span>
                              Published{" "}
                              {paper.publication_year ?? "N/A"}
                            </span>

                            <span>
                              Citations:{" "}
                              {paper.cited_by_count ?? 0}
                            </span>

                          </div>

                        </div>

                      </Link>

                    ),
                  )}

                </div>


                {/* ==============================================
                    PAGINATION
                    ============================================== */}

                {topicTotalPages > 1 && (

                  <div className="recommendation-pagination">

                    <button
                      type="button"
                      className="recommendation-pagination-button"
                      onClick={handlePreviousTopicPage}
                      disabled={
                        topicPage <= 1 ||
                        loading
                      }
                    >
                      ← Previous
                    </button>


                    <span className="recommendation-pagination-info">
                      Page{" "}
                      {topicPage}{" "}
                      of{" "}
                      {topicTotalPages}
                    </span>


                    <button
                      type="button"
                      className="recommendation-pagination-button"
                      onClick={handleNextTopicPage}
                      disabled={
                        topicPage >= topicTotalPages ||
                        loading
                      }
                    >
                      Next →
                    </button>

                  </div>

                )}

              </>

          )}


          {/* ==================================================
              EMPTY STATE
              ================================================== */}

          {!loading &&
            !error &&
            (
              view === "trending"
                ? trendingPapers.length === 0
                : view === "emerging"
                  ? emergingTopics.length === 0
                  : topicPapers.length === 0
            ) && (

              <div className="recommendation-empty">
                No results found.
              </div>

          )}

        </section>

      </div>

    </main>
  );
}

export default RecommendationsPage;