export interface PaperAuthor {
  readonly author_id: number;
  readonly author_name: string;
}

export interface PaperTopic {
  readonly topic_id: number;
  readonly topic_name: string;
}

export interface PaperListItem {
  readonly paper_id: number;
  readonly paper_name: string;
  readonly abstract?: string | null;
  readonly publication_year?: number | null;
  readonly publication_date?: string | null;
  readonly doi?: string | null;
  readonly cited_by_count?: number | null;
  readonly authors?: readonly PaperAuthor[];
  readonly topics?: readonly PaperTopic[];
}

export interface PaperDetail extends PaperListItem {
  readonly embedding?: readonly number[] | null;
}

export interface PaperSearchParams {
  readonly page?: number;
  readonly size?: number;
  readonly keyword?: string;
  readonly year?: number;
  readonly topic?: string;
  readonly author?: string;
}

export interface PaginatedPaperResponse {
  readonly items: readonly PaperListItem[];
  readonly total: number;
  readonly page: number;
  readonly size: number;
  readonly pages: number;

  // Backwards-compatible fields used by older frontend code
  readonly results: readonly PaperListItem[];
  readonly page_size: number;
}

// Backwards-compatible aliases
export type Author = PaperAuthor;
export type Topic = PaperTopic;
export type PaperListResponse = PaperListItem;
export type PaperList = PaperListItem;
export type PaperDetailResponse = PaperDetail;