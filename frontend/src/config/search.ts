// ============================================================
// Search Configuration
// ============================================================

export const SEARCH_CONFIG = {
  PAGE_SIZE: 20,
  DEBOUNCE_DELAY: 400,
  YEARS_RANGE: 50,
  CURRENT_YEAR: new Date().getFullYear(),
} as const;

// ============================================================
// Helper Functions
// ============================================================

export function generateYearArray(
  startYear: number,
  range: number,
): readonly number[] {
  const yearArray: number[] = [];
  for (let i = 0; i < range; i++) {
    yearArray.push(startYear - i);
  }
  return yearArray;
}
