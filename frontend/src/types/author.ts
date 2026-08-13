export interface Author {
  author_id: number;
  author_name: string;
  orcid: string | null;
}

export interface AuthorPaper {
  paper_id: number;
  paper_name: string;
  publication_year: number | null;
  cited_by_count: number | null;
}

export interface AuthorDetail {
  author_id: number;
  author_name: string;
  orcid: string | null;
  papers: AuthorPaper[];
}

export interface PaginatedAuthorResponse {
  page: number;
  page_size: number;
  total: number;
  results: Author[];
}