interface PaginationProps {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

export function Pagination({
  page,
  pageSize,
  total,
  onPageChange,
}: Readonly<PaginationProps>) {
  const totalPages = Math.ceil(
    total / pageSize,
  );

  if (totalPages <= 1) {
    return null;
  }

  const canGoPrevious = page > 1;
  const canGoNext = page < totalPages;

  return (
    <nav
      className="pagination"
      aria-label="Pagination"
    >
      <button
        type="button"
        disabled={!canGoPrevious}
        onClick={() =>
          onPageChange(page - 1)
        }
      >
        Previous
      </button>

      <span
        className="pagination__status"
        aria-current="page"
      >
        Page {page} of {totalPages}
      </span>

      <button
        type="button"
        disabled={!canGoNext}
        onClick={() =>
          onPageChange(page + 1)
        }
      >
        Next
      </button>
    </nav>
  );
}