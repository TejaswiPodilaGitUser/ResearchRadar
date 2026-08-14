/**
 * Topic summary.
 */
export interface Topic {
  topic_id: number;
  topic_name: string;
}

/**
 * Paper associated with a topic.
 */
export interface TopicPaper {
  paper_id: number;
  paper_name: string;
  publication_year: number | null;
  cited_by_count: number | null;
}

/**
 * Complete topic details.
 */
export interface TopicDetail extends Topic {
  papers: TopicPaper[];
}

/**
 * Paginated topic response.
 */
export interface PaginatedTopicResponse {
  results: Topic[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * Parameters for topic search.
 */
export interface TopicSearchParams {
  page?: number;
  size?: number;
  keyword?: string;
}

/**
 * Multiple topic response.
 *
 * The backend currently returns a dictionary
 * for multiple-topic endpoints.
 */
export type MultipleTopicResponse =
  Record<string, unknown>;