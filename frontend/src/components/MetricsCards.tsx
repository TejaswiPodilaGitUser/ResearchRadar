import type { MetricsResponse } from "../api/metrics";

interface MetricsCardsProps {
  metrics: MetricsResponse;
}

export default function MetricsCards({
  metrics,
}: MetricsCardsProps) {
  const yearRange =
    metrics.year_range.from !== null &&
    metrics.year_range.to !== null
      ? `${metrics.year_range.from} – ${metrics.year_range.to}`
      : "N/A";

  return (
    <div className="research-metrics-box">

      {/* Papers */}

      <div className="research-metric-row">
        <span>Papers</span>

        <strong>
          {metrics.papers.toLocaleString()}
        </strong>
      </div>


      {/* Authors */}

      <div className="research-metric-row">
        <span>Authors</span>

        <strong>
          {metrics.authors.toLocaleString()}
        </strong>
      </div>


      {/* Topics */}

      <div className="research-metric-row">
        <span>Topics</span>

        <strong>
          {metrics.topics.toLocaleString()}
        </strong>
      </div>


      {/* Publication Range */}

      <div className="research-metric-row">
        <span>Publication Range</span>

        <strong>
          {yearRange}
        </strong>
      </div>

    </div>
  );
}