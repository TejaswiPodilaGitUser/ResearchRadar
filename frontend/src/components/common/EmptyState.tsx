interface EmptyStateProps {
  title?: string;
  message?: string;
}

export function EmptyState({
  title = "No results found",
  message = "Try changing your search criteria.",
}: Readonly<EmptyStateProps>) {
  return (
    <section
      className="empty-state"
      aria-live="polite"
    >
      <h2>{title}</h2>
      <p>{message}</p>
    </section>
  );
}