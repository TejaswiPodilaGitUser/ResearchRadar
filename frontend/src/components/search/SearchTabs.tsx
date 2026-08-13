import { NavLink } from "react-router-dom";

const NAV_ITEMS = [
  {
    label: "Home",
    path: "/",
    icon: "⌂",
  },
  {
    label: "Papers",
    path: "/search",
    icon: "📄",
  },
  {
    label: "Authors",
    path: "/authors",
    icon: "👤",
  },
  {
    label: "Topics",
    path: "/topics",
    icon: "🏷",
  },
  {
    label: "Recommendations",
    path: "/recommendations",
    icon: "✦",
  },
  {
    label: "Trending",
    path: "/trending",
    icon: "↗",
  },
];

function SearchTabs() {
  return (
    <nav
      className="research-navigation"
      aria-label="Research Radar navigation"
    >
      <div className="research-navigation-inner">
        <div className="research-navigation-brand">
          <span className="research-brand-mark">
            R
          </span>

          <span className="research-brand-name">
            Research Radar
          </span>
        </div>

        <div className="research-navigation-links">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `research-nav-link ${
                  isActive
                    ? "research-nav-link-active"
                    : ""
                }`
              }
            >
              <span
                className="research-nav-icon"
                aria-hidden="true"
              >
                {item.icon}
              </span>

              <span>{item.label}</span>
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}

export default SearchTabs;

