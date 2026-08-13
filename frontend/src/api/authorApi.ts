import { httpClient } from "./axiosClient";

// ============================================================
// Author Types
// ============================================================

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

// ============================================================
// API Response Validation
// ============================================================

function isAuthor(
  value: unknown,
): value is Author {
  if (
    typeof value !== "object" ||
    value === null
  ) {
    return false;
  }

  const author =
    value as Record<string, unknown>;

  return (
    typeof author.author_id === "number" &&
    typeof author.author_name === "string"
  );
}

function isPaginatedAuthorResponse(
  value: unknown,
): value is PaginatedAuthorResponse {
  if (
    typeof value !== "object" ||
    value === null
  ) {
    return false;
  }

  const response =
    value as Record<string, unknown>;

  return (
    typeof response.page === "number" &&
    typeof response.page_size === "number" &&
    typeof response.total === "number" &&
    Array.isArray(response.results) &&
    response.results.every(isAuthor)
  );
}

// ============================================================
// Get Authors
// ============================================================

export async function getAuthors(
  searchValue: string,
  page = 1,
  size = 12,
): Promise<PaginatedAuthorResponse> {
  const value =
    searchValue.trim();

  if (!value) {
    throw new Error(
      "Author search value is required.",
    );
  }

  /*
   * Determine whether the user searched using
   * an author ID or an author name.
   *
   * Example:
   *
   * 123       -> author_id=123
   * Einstein  -> keyword=Einstein
   */

  const isAuthorId =
    /^\d+$/.test(value);

  const params: Record<
    string,
    string | number
  > = {
    page,
    size,
  };

  if (isAuthorId) {
    params.author_id =
      Number(value);
  } else {
    params.keyword = value;
  }

  console.log(
    "GET /api/authors params:",
    params,
  );

  const response =
    await httpClient.get<unknown>(
      "/api/authors",
      {
        params,
      },
    );

  console.log(
    "GET /api/authors response:",
    response.data,
  );

  // ==========================================================
  // Validate Response
  // ==========================================================

  if (
    !isPaginatedAuthorResponse(
      response.data,
    )
  ) {
    console.error(
      "Unexpected authors API response:",
      response.data,
    );

    throw new Error(
      "Invalid authors API response format.",
    );
  }

  return response.data;
}

// ============================================================
// Get Author By ID
// ============================================================

export async function getAuthorById(
  authorId: number,
): Promise<AuthorDetail> {
  if (
    !Number.isInteger(authorId) ||
    authorId <= 0
  ) {
    throw new Error(
      "Invalid author ID.",
    );
  }

  console.log(
    "GET /api/authors/:authorId",
    authorId,
  );

  const response =
    await httpClient.get<AuthorDetail>(
      `/api/authors/${authorId}`,
    );

  return response.data;
}

// ============================================================
// API Object
// ============================================================

export const authorApi = {
  getAuthors,
  getAuthorById,
};

