import { NavLink } from "react-router-dom";

import "../../styles/navigation.css";

const NAVIGATION_ITEMS = [
  {
    path: "/",
    label: "Home",
    icon: "⌂",
  },
  {
    path: "/papers",
    label: "Papers",
    icon: "📄",
  },
  {
    path: "/authors",
    label: "Authors",
    icon: "👤",
  },
  {
    path: "/topics",
    label: "Topics",
    icon: "🏷",
  },
  {
    path: "/recommendations",
    label: "Recommendations",
    icon: "🔥",
  },
] as const;

function MainNavigation() {
  return (
    <header className="main-navigation">
      <div className="navigation-container">

        <NavLink
          to="/"
          className="navigation-brand"
          aria-label="Research Radar Home"
        >
          <span
            className="brand-icon"
            aria-hidden="true"
          >
            R
          </span>

          <span className="brand-text">
            Research Radar
          </span>
        </NavLink>

        <nav
          className="navigation-tabs"
          aria-label="Main navigation"
        >
          {NAVIGATION_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `navigation-tab ${
                  isActive
                    ? "navigation-tab-active"
                    : ""
                }`
              }
            >
              <span
                className="navigation-tab-icon"
                aria-hidden="true"
              >
                {item.icon}
              </span>

              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

      </div>
    </header>
  );
}

export default MainNavigation;