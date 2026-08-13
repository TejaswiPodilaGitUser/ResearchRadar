import { useState } from "react";

import "../styles/entity-page.css";

function TopicsPage() {
  const [search, setSearch] = useState("");

  return (
    <main className="entity-page">
      <section className="entity-hero">
        <div className="entity-eyebrow">
          RESEARCH AREAS
        </div>

        <h1>Topics</h1>

        <p>
          Discover research areas, subjects, and
          emerging topics.
        </p>
      </section>

      <section className="entity-content">
        <div className="entity-search">
          <span>🏷</span>

          <input
            type="search"
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
            placeholder="Search by topic name or topic ID..."
          />
        </div>

        <div className="entity-empty">
          <div className="entity-empty-icon">
            🏷
          </div>

          <h2>Explore Topics</h2>

          <p>
            Search for a topic to discover related
            research papers.
          </p>
        </div>
      </section>
    </main>
  );
}

export default TopicsPage;
