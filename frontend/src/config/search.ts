// ============================================================
// Search Configuration
// ============================================================

export const SEARCH_CONFIG = {
  // Pagination
  PAGE_SIZE: 20,

  // Search
  MAX_SEARCH_RESULTS: 20,
  DEBOUNCE_DELAY: 400,

  // Search API endpoints
  SEMANTIC_SEARCH_ENDPOINT: "/api/search",
  HYBRID_SEARCH_ENDPOINT: "/api/search/hybrid",

  // Year filter
  YEARS_RANGE: 50,
  CURRENT_YEAR: new Date().getFullYear(),
} as const;


// ============================================================
// Search Modes
// ============================================================

export const SEARCH_MODE_OPTIONS = [
  {
    value: "keyword",
    label: "Exact search",
    description: "Find papers matching your words",
    actionLabel: "Search",
  },
  {
    value: "semantic",
    label: "Similar papers",
    description: "Find papers with similar meaning",
    actionLabel: "Find Similar Papers",
  },
  {
    value: "hybrid",
    label: "Smart search",
    description: "Combine exact matches with similar research",
    actionLabel: "Smart Search",
  },
] as const;


// ============================================================
// Search Mode Type
// ============================================================

export type SearchMode =
  (typeof SEARCH_MODE_OPTIONS)[number]["value"];


// ============================================================
// Helper
// ============================================================

export function generateYearArray(
  startYear: number,
  range: number,
): readonly number[] {
  const years: number[] = [];

  for (let i = 0; i < range; i += 1) {
    years.push(startYear - i);
  }

  return years;
}