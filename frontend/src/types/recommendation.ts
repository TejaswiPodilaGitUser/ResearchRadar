// ============================================================
// Recommendation Paper
// ============================================================

export type RecommendationPaper = {
  paper_id: number;
  paper_name: string;
  publication_year: number | null;
  cited_by_count: number;
};


// ============================================================
// Emerging Topic
// ============================================================

export type EmergingTopic = {
  topic_id: number;
  topic_name: string;

  paper_count: number;
  recent_paper_count: number;
  citation_count: number;
};


// ============================================================
// Top Author
// ============================================================

export type TopAuthor = {
  author_id: number;
  author_name: string;

  paper_count: number;
  citation_count: number;
};




// ============================================================
// Topic Papers Response
// ============================================================

export type TopicPapersResponse = {
  topic_id: number;
  topic_name: string;

  page: number;
  limit: number;

  total: number;
  total_pages: number;

  has_previous: boolean;
  has_next: boolean;

  results: RecommendationPaper[];
};