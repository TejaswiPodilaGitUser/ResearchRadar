// ============================================================
// Paper Types
// ============================================================

export interface Author {
  author_id: number;
  author_name: string;
}

export interface Topic {
  topic_id: number;
  topic_name: string;
}


// ============================================================
// Paper List Item
// ============================================================

export interface PaperListItem {
  paper_id: number;
  paper_name: string;
  publication_year: number | null;
  cited_by_count: number | null;
  abstract?: string | null;
  authors: Author[];
}


// ============================================================
// Paper Detail
// ============================================================

export interface PaperDetail extends PaperListItem {
  doi?: string | null;
  topics?: Topic[];
}


// ============================================================
// Search Parameters
// ============================================================

export interface PaperSearchParams {
  page?: number;
  size?: number;

  paper_id?: number;
  paper_ids?: number[];

  keyword?: string;

  paper_name?: string;
  paper_names?: string[];

  year?: number;
  topic?: string;
  author?: string;
}


// ============================================================
// Paginated Response
// ============================================================

export interface PaginatedPaperResponse {
  page: number;
  page_size: number;
  total: number;
  results: PaperListItem[];
}


// ============================================================
// Collection Response
// ============================================================

export interface PaperCollectionResponse {
  results: PaperDetail[];
  requested_count: number;
  returned_count: number;
}