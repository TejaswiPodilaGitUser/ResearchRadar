import {
  AxiosError,
} from "axios";

import {
  httpClient,
} from "./axiosClient";

import type {
  PaperCollectionResponse,
  PaperDetail,
  PaperSearchParams,
  PaginatedPaperResponse,
} from "../types/paper";


// ============================================================
// API Error
// ============================================================

export class PaperApiError extends Error {
  status: number | undefined;

  constructor(
    message: string,
    status?: number,
  ) {
    super(message);

    this.name = "PaperApiError";
    this.status = status;

    Object.setPrototypeOf(
      this,
      PaperApiError.prototype,
    );
  }
}


// ============================================================
// Error Helper
// ============================================================

function createPaperApiError(
  error: unknown,
  fallback: string,
): PaperApiError {
  if (error instanceof PaperApiError) {
    return error;
  }


  if (error instanceof AxiosError) {
    const status =
      error.response?.status;


    // ----------------------------------------------------------
    // 404
    // ----------------------------------------------------------

    if (status === 404) {
      return new PaperApiError(
        "Paper does not exist.",
        404,
      );
    }


    // ----------------------------------------------------------
    // API error message
    // ----------------------------------------------------------

    const data =
      error.response?.data;


    if (
      data &&
      typeof data === "object"
    ) {
      const detail =
        "detail" in data
          ? data.detail
          : undefined;

      const message =
        "message" in data
          ? data.message
          : undefined;


      if (
        typeof detail === "string" &&
        detail.trim()
      ) {
        return new PaperApiError(
          detail,
          status,
        );
      }


      if (
        typeof message === "string" &&
        message.trim()
      ) {
        return new PaperApiError(
          message,
          status,
        );
      }
    }


    return new PaperApiError(
      fallback,
      status,
    );
  }


  if (error instanceof Error) {
    return new PaperApiError(
      fallback,
    );
  }


  return new PaperApiError(
    fallback,
  );
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
  } catch (error: unknown) {
    throw createPaperApiError(
      error,
      "Unable to search papers.",
    );
  }
}


// ============================================================
// Get Paper By ID
// ============================================================

export async function getPaperById(
  paperId: number,
): Promise<PaperDetail> {
  if (
    !Number.isInteger(paperId) ||
    paperId <= 0
  ) {
    throw new PaperApiError(
      "Invalid paper ID.",
    );
  }


  try {
    const response =
      await httpClient.get<PaperDetail>(
        `/api/papers/${paperId}`,
      );

    return response.data;
  } catch (error: unknown) {
    throw createPaperApiError(
      error,
      "Unable to find the paper.",
    );
  }
}


// ============================================================
// Get Paper By Name
// ============================================================

export async function getPaperByName(
  paperName: string,
): Promise<PaperDetail> {
  const name =
    paperName.trim();


  if (!name) {
    throw new PaperApiError(
      "Paper name is required.",
    );
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
  } catch (error: unknown) {
    throw createPaperApiError(
      error,
      "Unable to find the paper.",
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
    throw new PaperApiError(
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
  } catch (error: unknown) {
    throw createPaperApiError(
      error,
      "Unable to find the requested papers.",
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
        .map(
          (name) =>
            name.trim(),
        )
        .filter(Boolean),
    ),
  ];


  if (names.length === 0) {
    throw new PaperApiError(
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
  } catch (error: unknown) {
    throw createPaperApiError(
      error,
      "Unable to find the requested papers.",
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
