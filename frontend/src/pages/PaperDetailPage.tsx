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
  getPaperById,
  PaperApiError,
} from "../api/paperApi";

import {
  getSimilarPapers,
} from "../api/recommendationApi";

import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import PaperCard from "../components/papers/PaperCard";

import type {
  PaperDetail,
} from "../types/paper";


/* ============================================================
   Constants
   ============================================================ */

const SIMILAR_PAPER_LIMIT = 5;

const NOT_FOUND_MESSAGE =
  "Try with a different paper ID or name.";

const GENERIC_ERROR_MESSAGE =
  "We couldn't load this paper. Please try again.";


/* ============================================================
   Helpers
   ============================================================ */

/**
 * Converts the route parameter into a valid positive integer.
 *
 * Returns null when the value is missing or invalid.
 */
const parsePaperId = (
  paperId: string | undefined,
): number | null => {

  if (!paperId) {
    return null;
  }

  const id = Number(paperId);

  if (
    !Number.isInteger(id) ||
    id <= 0
  ) {
    return null;
  }

  return id;
};


/**
 * Returns the appropriate user-facing error message
 * for a failed paper API request.
 */
const getPaperErrorMessage = (
  error: unknown,
): string => {

  if (
    error instanceof PaperApiError &&
    error.status === 404
  ) {
    return "Paper does not exist.";
  }

  if (
    error instanceof PaperApiError
  ) {
    return (
      error.message ||
      GENERIC_ERROR_MESSAGE
    );
  }

  return GENERIC_ERROR_MESSAGE;
};


/**
 * Loads similar papers for the selected paper.
 *
 * Similar papers are optional. A failure here should never
 * cause the main paper detail page to fail.
 */
const loadSimilarPapers = async (
  paperId: number,
  isCancelled: () => boolean,
): Promise<PaperDetail[]> => {

  try {
    const response =
      await getSimilarPapers(
        paperId,
        SIMILAR_PAPER_LIMIT,
      );

    if (isCancelled()) {
      return [];
    }

    return response ?? [];

  } catch (error: unknown) {

    console.error(
      "Failed to load similar papers:",
      error,
    );

    return [];
  }
};


/* ============================================================
   Page
   ============================================================ */

function PaperDetailPage() {

  const {
    paperId,
  } = useParams<{
    paperId: string;
  }>();

  const navigate = useNavigate();


  /* ==========================================================
     State
     ========================================================== */

  const [
    paper,
    setPaper,
  ] = useState<PaperDetail | null>(null);

  const [
    similarPapers,
    setSimilarPapers,
  ] = useState<PaperDetail[]>([]);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    similarLoading,
    setSimilarLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  /* ==========================================================
     Load Paper
     ========================================================== */

  useEffect(() => {

    let cancelled = false;


    const load = async (): Promise<void> => {

      /* ------------------------------------------------------
         Reset state
         ------------------------------------------------------ */

      setLoading(true);
      setError(null);
      setPaper(null);
      setSimilarPapers([]);
      setSimilarLoading(false);


      /* ------------------------------------------------------
         Validate route parameter
         ------------------------------------------------------ */

      if (!paperId) {

        if (!cancelled) {
          setError(
            "Paper ID is missing.",
          );

          setLoading(false);
        }

        return;
      }


      const id = parsePaperId(
        paperId,
      );


      if (id === null) {

        if (!cancelled) {
          setError(
            "Invalid paper ID.",
          );

          setLoading(false);
        }

        return;
      }


      /* ------------------------------------------------------
         Fetch paper
         ------------------------------------------------------ */

      try {

        const response =
          await getPaperById(id);


        if (cancelled) {
          return;
        }


        /* ----------------------------------------------------
           Validate response
           ---------------------------------------------------- */

        if (!response) {

          setError(
            "Paper does not exist.",
          );

          setLoading(false);

          return;
        }


        /* ----------------------------------------------------
           Store paper
           ---------------------------------------------------- */

        setPaper(response);
        setLoading(false);


        /* ----------------------------------------------------
           Load similar papers
           ---------------------------------------------------- */

        setSimilarLoading(true);


        const similar =
          await loadSimilarPapers(
            id,
            () => cancelled,
          );


        if (cancelled) {
          return;
        }


        setSimilarPapers(
          similar,
        );

        setSimilarLoading(false);

      } catch (err: unknown) {

        if (cancelled) {
          return;
        }


        console.error(
          "Failed to load paper:",
          err,
        );


        setError(
          getPaperErrorMessage(err),
        );

        setLoading(false);
        setSimilarLoading(false);
      }
    };


    void load();


    return () => {
      cancelled = true;
    };

  }, [paperId]);


  /* ==========================================================
     Navigation
     ========================================================== */

  const handleRetry = (): void => {

    navigate(
      "/papers",
      {
        replace: true,
      },
    );
  };


  const handleSimilarPaperClick = (
    similarPaperId: number,
  ): void => {

    navigate(
      `/papers/${similarPaperId}`,
    );
  };


  /* ==========================================================
     Loading
     ========================================================== */

  if (loading) {

    return (
      <main className="paper-detail-page">

        <div className="paper-detail-container">

          <LoadingState
            message="Loading paper..."
          />

        </div>

      </main>
    );
  }


  /* ==========================================================
     Error
     ========================================================== */

  if (error) {

    const isNotFound =
      error === "Paper does not exist.";


    return (
      <main className="paper-detail-page">

        <div className="paper-detail-container">

          <ErrorState
            title={
              isNotFound
                ? "Paper does not exist"
                : "Something went wrong"
            }
            message={
              isNotFound
                ? NOT_FOUND_MESSAGE
                : error
            }
            onRetry={handleRetry}
          />

        </div>

      </main>
    );
  }


  /* ==========================================================
     Safety Check
     ========================================================== */

  if (!paper) {

    return (
      <main className="paper-detail-page">

        <div className="paper-detail-container">

          <ErrorState
            title="Paper does not exist"
            message={NOT_FOUND_MESSAGE}
            onRetry={handleRetry}
          />

        </div>

      </main>
    );
  }


  /* ==========================================================
     Render
     ========================================================== */

  return (
    <main className="paper-detail-page">

      <div className="paper-detail-container">


        {/* ==================================================
            Back Navigation
            ================================================== */}

        <Link
          to="/papers"
          className="paper-back-link"
        >
          <span aria-hidden="true">
            ←
          </span>

          <span>
            Back to Papers
          </span>
        </Link>


        {/* ==================================================
            Paper Header
            ================================================== */}

        <article className="paper-detail-card">

          <header className="paper-detail-header">

            <div className="paper-detail-eyebrow">
              Research Paper
            </div>


            <h1 className="paper-detail-title">
              {paper.paper_name}
            </h1>


            <div className="paper-detail-meta">

              {paper.publication_year && (
                <span className="paper-meta-item">

                  <span className="paper-meta-label">
                    Published
                  </span>

                  <span>
                    {paper.publication_year}
                  </span>

                </span>
              )}


              {paper.publication_year && (
                <span
                  className="paper-meta-divider"
                  aria-hidden="true"
                >
                  •
                </span>
              )}


              <span className="paper-meta-item">

                <span className="paper-meta-label">
                  Citations
                </span>

                <span>
                  {paper.cited_by_count ?? 0}
                </span>

              </span>

            </div>

          </header>


          {/* =================================================
              Abstract
              ================================================= */}

          <section className="paper-detail-section">

            <div className="paper-section-heading">
              Abstract
            </div>


            {paper.abstract ? (

              <p className="paper-abstract">
                {paper.abstract}
              </p>

            ) : (

              <p className="paper-muted">
                No abstract available.
              </p>

            )}

          </section>


          {/* =================================================
              Authors
              ================================================= */}

          <section className="paper-detail-section">

            <div className="paper-section-heading">
              Authors
            </div>


            {paper.authors &&
            paper.authors.length > 0 ? (

              <div className="paper-authors">

                {paper.authors.map(
                  (author) => (

                    <div
                      key={author.author_id}
                      className="paper-author"
                    >

                      <span
                        className="paper-author-avatar"
                        aria-hidden="true"
                      >
                        {author.author_name
                          ?.charAt(0)
                          ?.toUpperCase() || "A"}
                      </span>

                      <span className="paper-author-name">
                        {author.author_name}
                      </span>

                    </div>
                  ),
                )}

              </div>

            ) : (

              <p className="paper-muted">
                No authors available.
              </p>

            )}

          </section>


          {/* =================================================
              Topics
              ================================================= */}

          <section className="paper-detail-section">

            <div className="paper-section-heading">
              Topics
            </div>


            {paper.topics &&
            paper.topics.length > 0 ? (

              <div className="paper-topic-list">

                {paper.topics.map(
                  (topic) => (

                    <span
                      key={topic.topic_id}
                      className="paper-topic-tag"
                    >
                      {topic.topic_name}
                    </span>

                  ),
                )}

              </div>

            ) : (

              <p className="paper-muted">
                No topics available.
              </p>

            )}

          </section>


          {/* =================================================
              DOI
              ================================================= */}

          {paper.doi && (

            <section className="paper-detail-section">

              <div className="paper-section-heading">
                DOI
              </div>


              <a
                href={paper.doi}
                target="_blank"
                rel="noopener noreferrer"
                className="paper-doi-link"
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
          className="paper-recommendations"
          aria-labelledby="similar-papers-heading"
        >

          <header className="paper-recommendations-header">

            <div className="paper-recommendations-heading">

              <div className="paper-detail-eyebrow">
                Recommendations
              </div>

              <h2
                id="similar-papers-heading"
              >
                Similar Papers
              </h2>

              <p>
                Research papers with similar content
                from this corpus.
              </p>

            </div>

          </header>


          {/* ------------------------------------------------
              Loading
              ------------------------------------------------ */}

          {similarLoading && (

            <div className="paper-recommendations-loading">

              <LoadingState
                message="Finding similar papers..."
              />

            </div>

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
                    paper={
                      similarPaper
                    }
                    onClick={() =>
                      handleSimilarPaperClick(
                        similarPaper.paper_id,
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

            <div className="paper-recommendations-empty">
              No similar papers found.
            </div>

          )}

        </section>

      </div>

    </main>
  );
}


export default PaperDetailPage;