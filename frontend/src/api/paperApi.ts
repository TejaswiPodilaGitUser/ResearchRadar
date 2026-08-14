import { httpClient } from "./axiosClient";

import type {
  PaperCollectionResponse,
  PaperDetail,
  PaperSearchParams,
  PaginatedPaperResponse,
} from "../types/paper";

// ============================================================
// Error Helper
// ============================================================

function getApiErrorMessage(
  error: unknown,
  fallback: string,
): string {
  if (
    error &&
    typeof error === "object" &&
    "response" in error
  ) {
    const response = (
      error as {
        response?: {
          data?: {
            detail?: string;
            message?: string;
          };
        };
      }
    ).response;

    const detail =
      response?.data?.detail ??
      response?.data?.message;

    if (typeof detail === "string" && detail.trim()) {
      return detail;
    }
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return fallback;
}

// ============================================================
// Get Papers
// ============================================================

export async function getPapers(
  params: PaperSearchParams = {},
): Promise<PaginatedPaperResponse> {
  try {
    const response =
      await httpClient.get<PaginatedPaperResponse>(
        "/api/papers",
        {
          params,
        },
      );

    return response.data;
  } catch (error) {
    throw new Error(
      getApiErrorMessage(
        error,
        "Unable to search papers.",
      ),
    );
  }
}

// ============================================================
// Get Paper By ID
// ============================================================

export async function getPaperById(
  paperId: number,
): Promise<PaperDetail> {
  if (!Number.isInteger(paperId) || paperId <= 0) {
    throw new Error("Invalid paper ID.");
  }

  try {
    const response =
      await httpClient.get<PaperDetail>(
        `/api/papers/${paperId}`,
      );

    return response.data;
  } catch (error) {
    throw new Error(
      getApiErrorMessage(
        error,
        "Unable to find the paper.",
      ),
    );
  }
}

// ============================================================
// Get Paper By Name
// ============================================================

export async function getPaperByName(
  paperName: string,
): Promise<PaperDetail> {
  const name = paperName.trim();

  if (!name) {
    throw new Error("Paper name is required.");
  }

  try {
    const response =
      await httpClient.get<PaperDetail>(
        "/api/papers/name",
        {
          params: {
            name,
          },
        },
      );

    return response.data;
  } catch (error) {
    throw new Error(
      getApiErrorMessage(
        error,
        "Unable to find the paper.",
      ),
    );
  }
}

// ============================================================
// Get Papers By IDs
// ============================================================

export async function getPapersByIds(
  paperIds: number[],
): Promise<PaperCollectionResponse> {
  const uniqueIds = [
    ...new Set(
      paperIds.filter(
        (id) =>
          Number.isInteger(id) &&
          id > 0,
      ),
    ),
  ];

  if (uniqueIds.length === 0) {
    throw new Error(
      "At least one valid paper ID is required.",
    );
  }

  try {
    const response =
      await httpClient.get<PaperCollectionResponse>(
        "/api/papers/collection/ids",
        {
          params: {
            ids: uniqueIds.join(","),
          },
        },
      );

    return response.data;
  } catch (error) {
    throw new Error(
      getApiErrorMessage(
        error,
        "Unable to find the requested papers.",
      ),
    );
  }
}

// ============================================================
// Get Papers By Names
// ============================================================

export async function getPapersByNames(
  paperNames: string[],
): Promise<PaperCollectionResponse> {
  const names = [
    ...new Set(
      paperNames
        .map((name) => name.trim())
        .filter(Boolean),
    ),
  ];

  if (names.length === 0) {
    throw new Error(
      "At least one paper name is required.",
    );
  }

  try {
    const response =
      await httpClient.get<PaperCollectionResponse>(
        "/api/papers/collection/names",
        {
          params: {
            names: names.join(","),
          },
        },
      );

    return response.data;
  } catch (error) {
    throw new Error(
      getApiErrorMessage(
        error,
        "Unable to find the requested papers.",
      ),
    );
  }
}

// ============================================================
// API Object
// ============================================================

export const paperApi = {
  getPapers,
  getPaperById,
  getPaperByName,
  getPapersByIds,
  getPapersByNames,
};