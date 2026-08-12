import { useEffect, useState } from "react";

import {
  getApiMetrics,
  type ApiMetricsResponse,
} from "../api/apiMetrics";

import "../styles/api-metrics.css";

export default function ApiMetrics() {
  const [metrics, setMetrics] =
    useState<ApiMetricsResponse | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function loadMetrics() {
      try {
        setLoading(true);
        setError(null);

        const data = await getApiMetrics();

        if (mounted) {
          setMetrics(data);
        }
      } catch (err) {
        console.error(
          "Failed to load API metrics:",
          err,
        );

        if (mounted) {
          setError(
            "Unable to load API metrics.",
          );
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadMetrics();

    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return (
      <section className="api-metrics-section">
        <div className="api-metrics-header">
          <h2>API Performance</h2>
          <p>
            Application API health and performance.
          </p>
        </div>

        <div className="api-metrics-state">
          Loading API metrics...
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="api-metrics-section">
        <div className="api-metrics-header">
          <h2>API Performance</h2>
          <p>
            Application API health and performance.
          </p>
        </div>

        <div className="api-metrics-error">
          {error}
        </div>
      </section>
    );
  }

  if (!metrics) {
    return (
      <section className="api-metrics-section">
        <div className="api-metrics-header">
          <h2>API Performance</h2>
          <p>
            Application API health and performance.
          </p>
        </div>

        <div className="api-metrics-state">
          No API metrics available.
        </div>
      </section>
    );
  }

  return (
    <section className="api-metrics-section">

      <div className="api-metrics-header">
        <h2>API Performance</h2>

        <p>
          Application API health and performance.
        </p>
      </div>

      {/* Main Metrics */}

      <div className="api-metrics-box">

        <div className="api-metric-row">
          <span>Requests</span>
          <strong>
            {metrics.requests.toLocaleString()}
          </strong>
        </div>

        <div className="api-metric-row">
          <span>Avg Response</span>
          <strong>
            {metrics.avg_response_ms} ms
          </strong>
        </div>

        <div className="api-metric-row">
          <span>Errors</span>
          <strong>
            {metrics.errors.toLocaleString()}
          </strong>
        </div>

        <div className="api-metric-row">
          <span>Error Rate</span>
          <strong>
            {metrics.error_rate}%
          </strong>
        </div>

      </div>


      {/* Latency */}

      <div className="api-latency-section">

        <h3>Latency</h3>

        <div className="api-metrics-box">

          <div className="api-metric-row">
            <span>P90 Latency</span>
            <strong>
              {metrics.p90_latency_ms} ms
            </strong>
          </div>

          <div className="api-metric-row">
            <span>P95 Latency</span>
            <strong>
              {metrics.p95_latency_ms} ms
            </strong>
          </div>

          <div className="api-metric-row">
            <span>P99 Latency</span>
            <strong>
              {metrics.p99_latency_ms} ms
            </strong>
          </div>

        </div>

      </div>

    </section>
  );
}