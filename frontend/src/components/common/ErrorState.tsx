interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = "Something went wrong",
  message = "We couldn't complete your request. Please try again.",
  onRetry,
}: Readonly<ErrorStateProps>) {
  return (
    <section
      className="error-state"
      role="alert"
    >
      <div className="error-state-content">
        <h2>{title}</h2>

        <p>{message}</p>

        {onRetry !== undefined && (
          <button
            type="button"
            className="error-state-button"
            onClick={onRetry}
          >
            Try Again
          </button>
        )}
      </div>
    </section>
  );
}

export default ErrorState;
