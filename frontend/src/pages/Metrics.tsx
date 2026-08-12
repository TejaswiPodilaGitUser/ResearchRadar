import { useEffect, useState } from "react";

import {
  getMetrics,
  type MetricsResponse,
} from "../api/metrics";

import MetricsCards from "../components/MetricsCards";
import ApiMetrics from "../components/ApiMetrics";

import "../styles/metrics.css";

export default function Metrics() {
  const [metrics, setMetrics] =
    useState<MetricsResponse | null>(null);

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

        const data = await getMetrics();

        if (mounted) {
          setMetrics(data);
        }
      } catch (err) {
        console.error(
          "Failed to load metrics:",
          err,
        );

        if (mounted) {
          setError(
            "Unable to load metrics. Please try again.",
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

  return (
    <main className="metrics-page">
      <div className="metrics-container">

        {/* =====================================================
            Page Header
            ===================================================== */}

        <header className="metrics-header">
          <h1>Research Radar Metrics</h1>

          <p>
            Overview of the research corpus.
          </p>
        </header>


        {/* =====================================================
            Loading
            ===================================================== */}

        {loading && (
          <div className="metrics-state">
            Loading metrics...
          </div>
        )}


        {/* =====================================================
            Error
            ===================================================== */}

        {!loading && error && (
          <div className="metrics-error">
            {error}
          </div>
        )}


        {/* =====================================================
            Research Corpus Metrics
            ===================================================== */}

        {!loading && !error && metrics && (
          <>
            <section className="research-metrics-section">

              <div className="research-metrics-header">
                <h2>Research Corpus</h2>

                <p>
                  Overview of the available research data.
                </p>
              </div>

              <MetricsCards metrics={metrics} />

            </section>


            {/* =================================================
                API Performance
                ================================================= */}

            <ApiMetrics />
          </>
        )}


        {/* =====================================================
            Empty
            ===================================================== */}

        {!loading && !error && !metrics && (
          <div className="metrics-state">
            No metrics available.
          </div>
        )}

      </div>
    </main>
  );
}