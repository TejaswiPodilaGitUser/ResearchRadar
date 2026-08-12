interface LoadingStateProps {
  readonly message?: string;
}

export function LoadingState({
  message = "Loading...",
}: Readonly<LoadingStateProps>) {
  return (
    <section
      className="loading-state"
      aria-live="polite"
      aria-busy="true"
    >
      <div
        className="loading-state__spinner"
        aria-hidden="true"
      />

      <p>{message}</p>
    </section>
  );
}

export default LoadingState;