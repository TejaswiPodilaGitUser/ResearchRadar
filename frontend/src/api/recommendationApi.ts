import { axiosClient } from "./axiosClient";

import type {
  EmergingTopic,
  RecommendationPaper,
  RecommendationListResponse,
} from "../types/recommendation";


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


// ============================================================
// Trending Papers
// ============================================================

export async function getTrendingPapers(
  limit = 10,
): Promise<RecommendationPaper[]> {

  const response =
    await axiosClient.get<RecommendationPaper[]>(
      "/api/recommendations/trending",
      {
        params: {
          limit,
        },
      },
    );

  return response.data;
}


// ============================================================
// Emerging Topics
// ============================================================

export async function getEmergingTopics(
  limit = 10,
): Promise<EmergingTopic[]> {

  const response =
    await axiosClient.get<EmergingTopic[]>(
      "/api/recommendations/emerging-topics",
      {
        params: {
          limit,
        },
      },
    );

  return response.data;
}


// ============================================================
// Papers By Topic
// ============================================================

export async function getPapersByTopic(
  topicId: number,
  page = 1,
  limit = 10,
): Promise<TopicPapersResponse> {

  const response =
    await axiosClient.get<TopicPapersResponse>(
      `/api/recommendations/topics/${topicId}/papers`,
      {
        params: {
          page,
          limit,
        },
      },
    );

  return response.data;
}


// ============================================================
// Similar Papers
// ============================================================

export async function getSimilarPapers(
  paperId: number,
  limit = 10,
): Promise<RecommendationPaper[]> {

  const response =
    await axiosClient.get<RecommendationListResponse>(
      `/api/recommendations/papers/${paperId}/similar`,
      {
        params: {
          limit,
        },
      },
    );

  return response.data.results;
}


// ============================================================
// Similar Papers By Topic
// ============================================================

export async function getSimilarPapersByTopic(
  topicId: number,
  limit = 10,
): Promise<RecommendationPaper[]> {

  const response =
    await axiosClient.get<RecommendationListResponse>(
      `/api/recommendations/topics/${topicId}/similar`,
      {
        params: {
          limit,
        },
      },
    );

  return response.data.results;
}