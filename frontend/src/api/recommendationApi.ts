import { axiosClient } from "./axiosClient";

import type { PaperDetail } from "../types/paper";

// ============================================================
// Similar Papers
// ============================================================

export async function getSimilarPapers(
  paperId: number,
  limit = 5,
): Promise<PaperDetail[]> {
  const response =
    await axiosClient.get<{
      results: PaperDetail[];
    }>(
      `/api/recommendations/${paperId}/similar`,
      {
        params: {
          limit,
        },
      },
    );

  return response.data.results;
}

// ============================================================
// Trending Papers
// ============================================================

export async function getTrendingPapers(
  limit = 10,
): Promise<PaperDetail[]> {
  const response =
    await axiosClient.get<PaperDetail[]>(
      "/api/recommendations/trending",
      {
        params: {
          limit,
        },
      },
    );

  return response.data;
} // Note: trending endpoint returns array directly, not wrapped in { results }

// ============================================================
// Topic Recommendations
// ============================================================

export async function getTopicRecommendations(
  paperId: number,
  limit = 10,
): Promise<PaperDetail[]> {
  const response =
    await axiosClient.get<{
      results: PaperDetail[];
    }>(
      `/api/recommendations/${paperId}/by-topic`,
      {
        params: {
          limit,
        },
      },
    );

  return response.data.results;
}

// ============================================================
// Author Recommendations
// ============================================================

export async function getAuthorRecommendations(
  paperId: number,
  limit = 10,
): Promise<PaperDetail[]> {
  const response =
    await axiosClient.get<{
      results: PaperDetail[];
    }>(
      `/api/recommendations/${paperId}/by-author`,
      {
        params: {
          limit,
        },
      },
    );

  return response.data.results;
}

// ============================================================
// All Recommendations
// ============================================================

export async function getRecommendations(
  paperId: number,
  limit = 10,
): Promise<PaperDetail[]> {
  const response =
    await axiosClient.get<{
      results: PaperDetail[];
    }>(
      `/api/recommendations/${paperId}`,
      {
        params: {
          limit,
        },
      },
    );

  return response.data.results;
}