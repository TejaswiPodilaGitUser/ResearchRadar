import axios from "axios";

import type {
  PaperDetail,
} from "../types/paper";


// ============================================================
// Axios
// ============================================================

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});


// ============================================================
// Types
// ============================================================

export interface RecommendationPaper {
  id: number;
  title: string;
  publication_year: number | null;
  doi: string | null;
  cited_by_count: number;
}


export interface RecommendationAuthor {
  author_id: number;
  author_name: string;
  paper_count: number;
  citation_count: number;
}


export interface RecommendationTopic {
  topic_id: number;
  topic_name: string;
  paper_count: number;
}


export interface TopicPapersResponse {
  topic_id: number;
  topic_name: string;

  page: number;
  limit: number;

  total: number;
  total_pages: number;

  has_previous: boolean;
  has_next: boolean;

  results: RecommendationPaper[];
}


// ============================================================
// Author Papers Response
// ============================================================

export interface AuthorPapersResponse {
  author_id: number;
  author_name: string;

  page: number;
  limit: number;

  total: number;
  total_pages: number;

  has_previous: boolean;
  has_next: boolean;

  results: RecommendationPaper[];
}


// ============================================================
// Emerging Topic
// ============================================================

export interface EmergingTopic {
  topic_id: number;
  topic_name: string;
  paper_count: number;
  recent_paper_count: number;
  citation_count: number;
}


// ============================================================
// Helpers
// ============================================================

const getErrorMessage = (
  error: unknown,
  fallback: string,
): string => {

  if (
    axios.isAxiosError(error)
  ) {
    const detail =
      error.response?.data?.detail;

    if (
      typeof detail === "string" &&
      detail.trim()
    ) {
      return detail;
    }

    if (
      typeof error.message === "string" &&
      error.message.trim()
    ) {
      return error.message;
    }
  }

  if (
    error instanceof Error &&
    error.message
  ) {
    return error.message;
  }

  return fallback;
};


// ============================================================
// Trending Papers
// ============================================================

export async function getTrendingPapers(
  limit: number = 10,
): Promise<RecommendationPaper[]> {

  try {

    const response =
      await api.get<RecommendationPaper[]>(
        "/recommendations/trending",
        {
          params: {
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );

    return response.data ?? [];

  } catch (error: unknown) {

    throw new Error(
      getErrorMessage(
        error,
        "Unable to load trending papers.",
      ),
    );
  }
}


// ============================================================
// Emerging Topics
// ============================================================

export async function getEmergingTopics(
  limit: number = 10,
): Promise<EmergingTopic[]> {

  try {

    const response =
      await api.get<EmergingTopic[]>(
        "/recommendations/emerging-topics",
        {
          params: {
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );

    return response.data ?? [];

  } catch (error: unknown) {

    throw new Error(
      getErrorMessage(
        error,
        "Unable to load emerging topics.",
      ),
    );
  }
}


// ============================================================
// Top Authors
// ============================================================

export async function getTopAuthors(
  limit: number = 10,
): Promise<RecommendationAuthor[]> {

  try {

    const response =
      await api.get<RecommendationAuthor[]>(
        "/recommendations/authors",
        {
          params: {
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );

    return response.data ?? [];

  } catch (error: unknown) {

    throw new Error(
      getErrorMessage(
        error,
        "Unable to load top authors.",
      ),
    );
  }
}


// ============================================================
// Topics
// ============================================================

export async function getRecommendationTopics(
  limit: number = 10,
): Promise<RecommendationTopic[]> {

  try {

    const response =
      await api.get<RecommendationTopic[]>(
        "/recommendations/topics",
        {
          params: {
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );

    return response.data ?? [];

  } catch (error: unknown) {

    throw new Error(
      getErrorMessage(
        error,
        "Unable to load topics.",
      ),
    );
  }
}


// ============================================================
// Papers By Topic
// ============================================================

export async function getPapersByTopic(
  topicId: number,
  page: number = 1,
  limit: number = 10,
): Promise<TopicPapersResponse> {

  try {

    const response =
      await api.get<TopicPapersResponse>(
        `/recommendations/topics/${topicId}/papers`,
        {
          params: {
            page: Math.max(page, 1),
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );

    return response.data;

  } catch (error: unknown) {

    throw new Error(
      getErrorMessage(
        error,
        "Unable to load papers for this topic.",
      ),
    );
  }
}


// ============================================================
// Papers By Author
// ============================================================

export async function getPapersByAuthor(
  authorId: number,
  page: number = 1,
  limit: number = 10,
): Promise<AuthorPapersResponse> {

  try {

    const response =
      await api.get<AuthorPapersResponse>(
        `/recommendations/authors/${authorId}/papers`,
        {
          params: {
            page: Math.max(page, 1),
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );

    return response.data;

  } catch (error: unknown) {

    throw new Error(
      getErrorMessage(
        error,
        "Unable to load papers for this author.",
      ),
    );
  }
}


// ============================================================
// Similar Papers
// ============================================================

export async function getSimilarPapers(
  paperId: number,
  limit: number = 5,
): Promise<PaperDetail[]> {

  try {

    const response =
      await api.get(
        `/recommendations/papers/${paperId}/similar`,
        {
          params: {
            limit: Math.min(
              Math.max(limit, 1),
              10,
            ),
          },
        },
      );


    const papers =
      Array.isArray(response.data)
        ? response.data
        : [];


    return papers
      .map((paper: any) => ({
        paper_id:
          paper.paper_id ??
          paper.id,

        paper_name:
          paper.paper_name ??
          paper.title ??
          "",

        publication_year:
          paper.publication_year ?? null,

        publication_date:
          paper.publication_date ?? null,

        cited_by_count:
          paper.cited_by_count ?? 0,

        doi:
          paper.doi ?? null,

        abstract:
          paper.abstract ?? null,

        authors:
          Array.isArray(paper.authors)
            ? paper.authors
            : [],

        topics:
          Array.isArray(paper.topics)
            ? paper.topics
            : [],

      }))
      .filter(
        (paper) =>
          Number.isInteger(
            paper.paper_id,
          ) &&
          paper.paper_id > 0,
      )
      .slice(0, limit);

  } catch (error) {

    console.error(
      "Failed to load similar papers:",
      error,
    );

    throw error;
  }
}