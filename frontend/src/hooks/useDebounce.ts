import { useEffect, useState } from "react";

/**
 * Delays updating a value until the specified
 * amount of time has elapsed without changes.
 */
export function useDebounce<T>(
  value: T,
  delay = 400
): T {
  const [debouncedValue, setDebouncedValue] =
    useState<T>(value);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      window.clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}