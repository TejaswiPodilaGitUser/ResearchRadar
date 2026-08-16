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
  getTopAuthors,
  getRecommendationTopics,
  getPapersByTopic,
  getPapersByAuthor,
} from "../api/recommendationApi";

import type {
  RecommendationPaper,
  RecommendationAuthor,
  RecommendationTopic,
  TopicPapersResponse,
  AuthorPapersResponse,
} from "../api/recommendationApi";


// ============================================================
// Types
// ============================================================

type RecommendationView =
  | "home"
  | "trending"
  | "emerging"
  | "authors"
  | "topics"
  | "topic-papers"
  | "author-papers";


interface EmergingTopic {
  topic_id: number;
  topic_name: string;
  paper_count: number;
  recent_paper_count?: number;
  citation_count?: number;
}


// ============================================================
// Page
// ============================================================

function RecommendationsPage() {

  const [
    view,
    setView,
  ] = useState<RecommendationView>("home");


  // ==========================================================
  // Data
  // ==========================================================

  const [
    trendingPapers,
    setTrendingPapers,
  ] = useState<RecommendationPaper[]>([]);


  const [
    emergingTopics,
    setEmergingTopics,
  ] = useState<EmergingTopic[]>([]);


  const [
    topAuthors,
    setTopAuthors,
  ] = useState<RecommendationAuthor[]>([]);


  const [
    topics,
    setTopics,
  ] = useState<RecommendationTopic[]>([]);


  const [
    topicPapers,
    setTopicPapers,
  ] = useState<RecommendationPaper[]>([]);


  const [
    authorPapers,
    setAuthorPapers,
  ] = useState<RecommendationPaper[]>([]);


  // ==========================================================
  // Selected Topic
  // ==========================================================

  const [
    selectedTopicId,
    setSelectedTopicId,
  ] = useState<number | null>(null);


  const [
    selectedTopicName,
    setSelectedTopicName,
  ] = useState("");


  // ==========================================================
  // Selected Author
  // ==========================================================

  const [
    selectedAuthorId,
    setSelectedAuthorId,
  ] = useState<number | null>(null);


  const [
    selectedAuthorName,
    setSelectedAuthorName,
  ] = useState("");


  // ==========================================================
  // Topic Pagination
  // ==========================================================

  const [
    topicPage,
    setTopicPage,
  ] = useState(1);


  const [
    topicTotalPages,
    setTopicTotalPages,
  ] = useState(0);


  const [
    topicTotal,
    setTopicTotal,
  ] = useState(0);


  // ==========================================================
  // Author Pagination
  // ==========================================================

  const [
    authorPage,
    setAuthorPage,
  ] = useState(1);


  const [
    authorTotalPages,
    setAuthorTotalPages,
  ] = useState(0);


  const [
    authorTotal,
    setAuthorTotal,
  ] = useState(0);


  // ==========================================================
  // Loading / Error
  // ==========================================================

  const [
    loading,
    setLoading,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState<string | null>(null);


  // ============================================================
  // Reset
  // ============================================================

  function resetState(): void {

    setError(null);
    setLoading(false);

  }


  // ============================================================
  // Trending
  // ============================================================

  async function handleTrending(): Promise<void> {

    setView("trending");

    setLoading(true);

    setError(null);

    try {

      const results =
        await getTrendingPapers(10);

      setTrendingPapers(results);

    } catch (err: unknown) {

      setTrendingPapers([]);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load trending papers.",
      );

    } finally {

      setLoading(false);

    }
  }


  // ============================================================
  // Emerging Topics
  // ============================================================

  async function handleEmergingTopics(): Promise<void> {

    setView("emerging");

    setLoading(true);

    setError(null);

    try {

      const results =
        await getEmergingTopics(10);

      setEmergingTopics(
        results as EmergingTopic[],
      );

    } catch (err: unknown) {

      setEmergingTopics([]);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load emerging topics.",
      );

    } finally {

      setLoading(false);

    }
  }


  // ============================================================
  // Top Authors
  // ============================================================

  async function handleTopAuthors(): Promise<void> {

    setView("authors");

    setLoading(true);

    setError(null);

    try {

      const results =
        await getTopAuthors(10);

      setTopAuthors(results);

    } catch (err: unknown) {

      setTopAuthors([]);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load top authors.",
      );

    } finally {

      setLoading(false);

    }
  }


  // ============================================================
  // Author Papers
  // ============================================================

  async function handleAuthorPapers(
    authorId: number,
    authorName: string,
    page: number = 1,
  ): Promise<void> {

    setView("author-papers");

    setLoading(true);

    setError(null);

    setSelectedAuthorId(authorId);

    setSelectedAuthorName(authorName);

    try {

      const response: AuthorPapersResponse =
        await getPapersByAuthor(
          authorId,
          page,
          10,
        );

      setAuthorPapers(
        response.results ?? [],
      );

      setAuthorPage(
        response.page,
      );

      setAuthorTotalPages(
        response.total_pages,
      );

      setAuthorTotal(
        response.total,
      );

    } catch (err: unknown) {

      setAuthorPapers([]);

      setAuthorTotalPages(0);

      setAuthorTotal(0);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load papers for this author.",
      );

    } finally {

      setLoading(false);

    }
  }


  // ============================================================
  // Previous Author Page
  // ============================================================

  function handlePreviousAuthorPage(): void {

    if (
      selectedAuthorId === null ||
      authorPage <= 1 ||
      loading
    ) {
      return;
    }

    void handleAuthorPapers(
      selectedAuthorId,
      selectedAuthorName,
      authorPage - 1,
    );
  }


  // ============================================================
  // Next Author Page
  // ============================================================

  function handleNextAuthorPage(): void {

    if (
      selectedAuthorId === null ||
      authorPage >= authorTotalPages ||
      loading
    ) {
      return;
    }

    void handleAuthorPapers(
      selectedAuthorId,
      selectedAuthorName,
      authorPage + 1,
    );
  }


  // ============================================================
  // Topics
  // ============================================================

  async function handleTopics(): Promise<void> {

    setView("topics");

    setLoading(true);

    setError(null);

    try {

      const results =
        await getRecommendationTopics(10);

      setTopics(results);

    } catch (err: unknown) {

      setTopics([]);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load topics.",
      );

    } finally {

      setLoading(false);

    }
  }


  // ============================================================
  // Topic Papers
  // ============================================================

  async function handleTopicPapers(
    topicId: number,
    topicName: string,
    page: number = 1,
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
        response.results ?? [],
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

    } catch (err: unknown) {

      setTopicPapers([]);

      setTopicTotalPages(0);

      setTopicTotal(0);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to load papers for this topic.",
      );

    } finally {

      setLoading(false);

    }
  }


  // ============================================================
  // Previous Topic Page
  // ============================================================

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


  // ============================================================
  // Next Topic Page
  // ============================================================

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


  // ============================================================
  // Back
  // ============================================================

  function handleBack(): void {

    setView("home");

    resetState();

    // Topic state
    setTopicPapers([]);

    setSelectedTopicId(null);

    setSelectedTopicName("");

    setTopicPage(1);

    setTopicTotalPages(0);

    setTopicTotal(0);

    // Author state
    setAuthorPapers([]);

    setSelectedAuthorId(null);

    setSelectedAuthorName("");

    setAuthorPage(1);

    setAuthorTotalPages(0);

    setAuthorTotal(0);

  }


  // ============================================================
  // Back From Topic Papers
  // ============================================================

  function handleBackFromTopicPapers(): void {

    setView("topics");

    setLoading(false);

    setError(null);

    setTopicPapers([]);

    setSelectedTopicId(null);

    setSelectedTopicName("");

    setTopicPage(1);

    setTopicTotalPages(0);

    setTopicTotal(0);

  }


  // ============================================================
  // Back From Author Papers
  // ============================================================

  function handleBackFromAuthorPapers(): void {

    setView("authors");

    setLoading(false);

    setError(null);

    setAuthorPapers([]);

    setSelectedAuthorId(null);

    setSelectedAuthorName("");

    setAuthorPage(1);

    setAuthorTotalPages(0);

    setAuthorTotal(0);

  }


  // ============================================================
  // Home
  // ============================================================

  if (view === "home") {

    return (
      <main className="recommendations-page">

        <div className="recommendations-container">

          <section className="recommendations-hero">

            <div className="recommendations-eyebrow">
              DISCOVERY
            </div>

            <h1>
              Recommendations
            </h1>

            <p>
              Discover trending research, emerging topics,
              leading authors, and research papers by topic.
            </p>

          </section>


          <section className="recommendation-grid">

            {/* ==================================================
                TRENDING
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
                Top 10 Trending Papers
              </h2>

              <p>
                Explore the research papers receiving
                the most citation attention.
              </p>

              <span className="recommendation-action">
                View Top 10 →
              </span>

            </button>


            {/* ==================================================
                EMERGING
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
                Top 10 Emerging Topics
              </h2>

              <p>
                Discover research topics showing
                increasing activity.
              </p>

              <span className="recommendation-action">
                View Top 10 →
              </span>

            </button>


            {/* ==================================================
                AUTHORS
                ================================================== */}

            <button
              type="button"
              className="recommendation-card"
              onClick={() => {
                void handleTopAuthors();
              }}
            >

              <div className="recommendation-icon">
                👥
              </div>

              <h2>
                Top 10 Authors
              </h2>

              <p>
                Find authors who have contributed
                multiple papers to the research corpus.
              </p>

              <span className="recommendation-action">
                View Top 10 →
              </span>

            </button>


            {/* ==================================================
                TOPICS
                ================================================== */}

            <button
              type="button"
              className="recommendation-card"
              onClick={() => {
                void handleTopics();
              }}
            >

              <div className="recommendation-icon">
                📚
              </div>

              <h2>
                Papers by Topic
              </h2>

              <p>
                Select a topic and browse its papers
                with pagination.
              </p>

              <span className="recommendation-action">
                Browse Topics →
              </span>

            </button>

          </section>

        </div>

      </main>
    );
  }


  // ============================================================
  // Results
  // ============================================================

  return (
    <main className="recommendations-page">

      <div className="recommendations-container">

        <section className="recommendations-hero">

          <button
            type="button"
            className="recommendation-back"
            onClick={
              view === "topic-papers"
                ? handleBackFromTopicPapers
                : view === "author-papers"
                  ? handleBackFromAuthorPapers
                  : handleBack
            }
          >
            {view === "topic-papers"
              ? "← Papers by Topic"
              : view === "author-papers"
                ? "← Top Authors"
                : "← Recommendations"}
          </button>


          <div className="recommendations-eyebrow">
            DISCOVERY
          </div>


          <h1>

            {view === "trending" &&
              "Top 10 Trending Papers"}

            {view === "emerging" &&
              "Top 10 Emerging Topics"}

            {view === "authors" &&
              "Top 10 Authors"}

            {view === "topics" &&
              "Papers by Topic"}

            {view === "topic-papers" &&
              selectedTopicName}

            {view === "author-papers" &&
              selectedAuthorName}

          </h1>


          <p>

            {view === "trending" &&
              "The research papers receiving the most citation attention."}

            {view === "emerging" &&
              "Research topics showing increasing activity."}

            {view === "authors" &&
              "Authors who have contributed multiple papers to the research corpus."}

            {view === "topics" &&
              "Select a topic to browse all papers associated with it."}

            {view === "topic-papers" &&
              `${topicTotal} papers associated with this topic.`}

            {view === "author-papers" &&
              `${authorTotal} papers associated with this author.`}

          </p>

        </section>


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
              TRENDING
              ================================================== */}

          {!loading &&
            !error &&
            view === "trending" && (

              <div className="recommendation-results">

                {trendingPapers.map(
                  (paper, index) => (

                    <Link
                      key={paper.id}
                      to={`/papers/${paper.id}`}
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
                          {paper.id}
                        </div>

                        <h2>
                          {paper.title}
                        </h2>

                        <div className="recommendation-card-meta">

                          <span>
                            Published{" "}
                            {paper.publication_year ?? "N/A"}
                          </span>

                          <span>
                            Citations:{" "}
                            {paper.cited_by_count}
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
                            {topic.paper_count ?? 0}
                          </span>

                          {topic.recent_paper_count !==
                            undefined && (
                            <span>
                              Recent:{" "}
                              {topic.recent_paper_count}
                            </span>
                          )}

                          {topic.citation_count !==
                            undefined && (
                            <span>
                              Citations:{" "}
                              {topic.citation_count}
                            </span>
                          )}

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
              AUTHORS
              ================================================== */}

          {!loading &&
            !error &&
            view === "authors" && (

              <div className="recommendation-results">

                {topAuthors.map(
                  (author, index) => (

                    <button
                      key={author.author_id}
                      type="button"
                      className="recommendation-result"
                      onClick={() => {
                        void handleAuthorPapers(
                          author.author_id,
                          author.author_name,
                          1,
                        );
                      }}
                    >

                      <div className="recommendation-rank">
                        {index + 1}
                      </div>

                      <div className="recommendation-result-content">

                        <div className="recommendation-card-label">
                          AUTHOR ID
                        </div>

                        <div className="recommendation-card-id">
                          {author.author_id}
                        </div>

                        <h2>
                          {author.author_name}
                        </h2>

                        <div className="recommendation-card-meta">

                          <span>
                            Papers:{" "}
                            {author.paper_count}
                          </span>

                          <span>
                            Citations:{" "}
                            {author.citation_count}
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
              TOPICS
              ================================================== */}

          {!loading &&
            !error &&
            view === "topics" && (

              <div className="recommendation-results">

                {topics.map(
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
                        key={paper.id}
                        to={`/papers/${paper.id}`}
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
                            {paper.id}
                          </div>

                          <h2>
                            {paper.title}
                          </h2>

                          <div className="recommendation-card-meta">

                            <span>
                              Published{" "}
                              {paper.publication_year ?? "N/A"}
                            </span>

                            <span>
                              Citations:{" "}
                              {paper.cited_by_count}
                            </span>

                          </div>

                        </div>

                      </Link>

                    ),
                  )}

                </div>


                {topicTotalPages > 1 && (

                  <div className="recommendation-pagination">

                    <button
                      type="button"
                      className="recommendation-pagination-button"
                      onClick={
                        handlePreviousTopicPage
                      }
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
                      onClick={
                        handleNextTopicPage
                      }
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
              AUTHOR PAPERS
              ================================================== */}

          {!loading &&
            !error &&
            view === "author-papers" && (

              <>

                <div className="recommendation-results">

                  {authorPapers.map(
                    (paper, index) => (

                      <Link
                        key={paper.id}
                        to={`/papers/${paper.id}`}
                        className="recommendation-result"
                      >

                        <div className="recommendation-rank">
                          {(
                            (authorPage - 1) * 10
                          ) + index + 1}
                        </div>

                        <div className="recommendation-result-content">

                          <div className="recommendation-card-label">
                            PAPER ID
                          </div>

                          <div className="recommendation-card-id">
                            {paper.id}
                          </div>

                          <h2>
                            {paper.title}
                          </h2>

                          <div className="recommendation-card-meta">

                            <span>
                              Published{" "}
                              {paper.publication_year ?? "N/A"}
                            </span>

                            <span>
                              Citations:{" "}
                              {paper.cited_by_count}
                            </span>

                          </div>

                        </div>

                      </Link>

                    ),
                  )}

                </div>


                {authorTotalPages > 1 && (

                  <div className="recommendation-pagination">

                    <button
                      type="button"
                      className="recommendation-pagination-button"
                      onClick={
                        handlePreviousAuthorPage
                      }
                      disabled={
                        authorPage <= 1 ||
                        loading
                      }
                    >
                      ← Previous
                    </button>


                    <span className="recommendation-pagination-info">
                      Page{" "}
                      {authorPage}{" "}
                      of{" "}
                      {authorTotalPages}
                    </span>


                    <button
                      type="button"
                      className="recommendation-pagination-button"
                      onClick={
                        handleNextAuthorPage
                      }
                      disabled={
                        authorPage >= authorTotalPages ||
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
              EMPTY
              ================================================== */}

          {!loading &&
            !error &&
            (
              (
                view === "trending" &&
                trendingPapers.length === 0
              ) ||

              (
                view === "emerging" &&
                emergingTopics.length === 0
              ) ||

              (
                view === "authors" &&
                topAuthors.length === 0
              ) ||

              (
                view === "topics" &&
                topics.length === 0
              ) ||

              (
                view === "topic-papers" &&
                topicPapers.length === 0
              ) ||

              (
                view === "author-papers" &&
                authorPapers.length === 0
              )
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