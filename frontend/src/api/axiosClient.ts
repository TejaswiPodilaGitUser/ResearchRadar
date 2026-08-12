import axios from "axios";

import { API_BASE_URL } from "../config/env";

export const httpClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15_000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

httpClient.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        console.error(
          `API request failed: ${error.response.status}`,
          error.response.data,
        );
      } else if (error.request) {
        console.error(
          "API request failed: no response received",
        );
      } else {
        console.error(
          "API request configuration failed:",
          error.message,
        );
      }
    }

    return Promise.reject(error);
  },
);

// Backwards-compatible export name used in some modules
export const axiosClient = httpClient;