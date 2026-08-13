import "../styles/entity-page.css";

function RecommendationsPage() {
  return (
    <main className="entity-page">
      <section className="entity-hero">
        <div className="entity-eyebrow">
          DISCOVERY
        </div>

        <h1>Recommendations</h1>

        <p>
          Discover trending and recommended research
          from the Research Radar corpus.
        </p>
      </section>

      <section className="entity-content">
        <div className="recommendation-grid">

          <article className="recommendation-card">
            <div className="recommendation-icon">
              🔥
            </div>

            <h2>Trending Research</h2>

            <p>
              Explore papers gaining attention across
              the research landscape.
            </p>
          </article>

          <article className="recommendation-card">
            <div className="recommendation-icon">
              ✦
            </div>

            <h2>Recommended Papers</h2>

            <p>
              Discover research related to your
              interests and searches.
            </p>
          </article>

          <article className="recommendation-card">
            <div className="recommendation-icon">
              📈
            </div>

            <h2>Emerging Topics</h2>

            <p>
              Find research areas showing increasing
              activity and interest.
            </p>
          </article>

        </div>
      </section>
    </main>
  );
}

export default RecommendationsPage;

