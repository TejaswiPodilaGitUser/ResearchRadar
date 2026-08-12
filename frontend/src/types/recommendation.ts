import type { Author, Topic } from "./paper";

export interface RecommendationPaper {
  paper_id: number;
  paper_name: string;

  abstract?: string | null;
  publication_year?: number | null;
  publication_date?: string | null;
  doi?: string | null;
  cited_by_count?: number | null;

  authors: Author[];
  topics: Topic[];
}

export interface RecommendationListResponse {
  results: RecommendationPaper[];
}

// Backwards-compatible aliases
export type RecommendationPaperResponse = RecommendationPaper;