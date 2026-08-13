import { httpClient } from "./axiosClient";

export interface Topic {
  id: number;
  name: string;
}

export interface TopicListResponse {
  results: Topic[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * Retrieve paginated topics.
 */
export async function getTopics(
  params: {
    page?: number;
    size?: number;
    name?: string;
  } = {},
): Promise<TopicListResponse> {
  const response =
    await httpClient.get<TopicListResponse>(
      "/api/topics",
      {
        params,
      },
    );

  return response.data;
}

/**
 * Retrieve a topic by ID.
 */
export async function getTopicById(
  topicId: number,
): Promise<Topic> {
  const response =
    await httpClient.get<Topic>(
      `/api/topics/${topicId}`,
    );

  return response.data;
}

export const topicApi = {
  getTopics,
  getTopicById,
};