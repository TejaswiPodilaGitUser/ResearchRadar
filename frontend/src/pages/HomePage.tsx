import { Link } from "react-router-dom";

import "../styles/home-page.css";

function HomePage() {
  return (
    <main className="home-page">
      <section className="home-hero">
        <div className="home-eyebrow">
          RESEARCH RADAR
        </div>

        <h1>
          Discover Research.
          <br />
          Explore Ideas.
        </h1>

        <p>
          Explore research papers, authors, topics,
          and emerging research trends in one place.
        </p>

        <Link
          to="/papers"
          className="home-search-button"
        >
          Start Exploring
        </Link>
      </section>
    </main>
  );
}

export default HomePage;

