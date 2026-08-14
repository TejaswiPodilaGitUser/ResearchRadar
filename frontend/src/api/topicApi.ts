import { httpClient } from "./axiosClient";

import type {
  MultipleTopicResponse,
  PaginatedTopicResponse,
  TopicDetail,
  TopicSearchParams,
} from "../types/topic";

/**
 * Retrieve paginated topics.
 */
export async function getTopics(
  params: TopicSearchParams = {},
): Promise<PaginatedTopicResponse> {
  const response =
    await httpClient.get<PaginatedTopicResponse>(
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
): Promise<TopicDetail> {
  const response =
    await httpClient.get<TopicDetail>(
      `/api/topics/${topicId}`,
    );

  return response.data;
}

/**
 * Retrieve a topic by exact name.
 */
export async function getTopicByName(
  name: string,
): Promise<TopicDetail> {
  const response =
    await httpClient.get<TopicDetail>(
      "/api/topics/name",
      {
        params: {
          name,
        },
      },
    );

  return response.data;
}

/**
 * Retrieve multiple topics by IDs.
 */
export async function getMultipleTopicsByIds(
  topicIds: number[],
): Promise<MultipleTopicResponse> {
  const response =
    await httpClient.get<MultipleTopicResponse>(
      "/api/topics/multiple/ids",
      {
        params: {
          ids: topicIds.join(","),
        },
      },
    );

  return response.data;
}

/**
 * Retrieve multiple topics by names.
 */
export async function getMultipleTopicsByNames(
  topicNames: string[],
): Promise<MultipleTopicResponse> {
  const response =
    await httpClient.get<MultipleTopicResponse>(
      "/api/topics/multiple/names",
      {
        params: {
          names: topicNames.join(","),
        },
      },
    );

  return response.data;
}

/**
 * Topic API.
 */
export const topicApi = {
  getTopics,
  getTopicById,
  getTopicByName,
  getMultipleTopicsByIds,
  getMultipleTopicsByNames,
};