/**
 * Dashboard.jsx
 * Central orchestrator — lifts all shared state up:
 *  - articles list + loading
 *  - stats + loading
 *  - selected article
 *  - pipeline running state
 *  - toast notifications
 *
 * Passes everything down to child components via props.
 */

import { useState, useEffect, useCallback } from "react";
import Navbar from "../components/Navbar";
import StatsCards from "../components/StatsCards";
import ChartsSection from "../components/ChartsSection";
import ArticlesTable from "../components/ArticlesTable";
import ArticleDetails from "../components/ArticleDetails";
import { Toast, useToast } from "../components/Toast";
import {
  fetchAllArticles,
  fetchStats,
  runPipeline,
} from "../services/api";

function Dashboard() {
  // ── State ──────────────────────────────────────────────────
  const [articles, setArticles] = useState([]);
  const [articlesLoading, setArticlesLoading] = useState(true);
  const [articlesError, setArticlesError] = useState("");

  const [stats, setStats] = useState(null);
  const [statsLoading, setStatsLoading] = useState(true);

  const [selectedArticle, setSelectedArticle] = useState(null);

  const [pipelineLoading, setPipelineLoading] = useState(false);
  const [city, setCity] = useState("Anantapur");

  const { toasts, addToast, removeToast } = useToast();

  // ── Data fetching ──────────────────────────────────────────
  const loadArticles = useCallback(async () => {
    try {
      setArticlesLoading(true);
      setArticlesError("");
      const res = await fetchAllArticles();
      setArticles(res.data.articles ?? []);

      // Keep selected article in sync with fresh data
      setSelectedArticle((prev) =>
        prev
          ? (res.data.articles ?? []).find((a) => a.hash === prev.hash) ?? prev
          : null
      );
    } catch (err) {
      console.error("Failed to load articles:", err);
      setArticlesError(
        err.response?.data?.detail ||
          "Could not connect to the backend. Is FastAPI running?"
      );
    } finally {
      setArticlesLoading(false);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      setStatsLoading(true);
      const res = await fetchStats();
      setStats(res.data);
    } catch (err) {
      console.error("Failed to load stats:", err);
    } finally {
      setStatsLoading(false);
    }
  }, []);

  // Refresh both articles and stats together
  const refresh = useCallback(async () => {
    await Promise.all([loadArticles(), loadStats()]);
  }, [loadArticles, loadStats]);

  // Initial load
  useEffect(() => {
    refresh();
  }, [refresh]);

  // Auto-refresh every 60 seconds
  useEffect(() => {
    const interval = setInterval(refresh, 60_000);
    return () => clearInterval(interval);
  }, [refresh]);

  // ── Pipeline ───────────────────────────────────────────────
  async function handleRunPipeline() {
    if (pipelineLoading) return;
    setPipelineLoading(true);
    addToast(`Running pipeline for "${city}"…`, "info");
    try {
      await runPipeline(city);
      addToast("Pipeline completed successfully! Refreshing data…", "success");
      await refresh();
    } catch (err) {
      addToast(
        `Pipeline failed: ${err.response?.data?.detail || err.message}`,
        "error"
      );
    } finally {
      setPipelineLoading(false);
    }
  }

  // ── Render ─────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* ── Navbar ────────────────────────────────────────── */}
      <Navbar
        onRunPipeline={handleRunPipeline}
        pipelineLoading={pipelineLoading}
        city={city}
        onCityChange={setCity}
      />

      {/* ── Main Content ──────────────────────────────────── */}
      <main className="max-w-screen-2xl mx-auto px-4 sm:px-6 py-8">

        {/* Page title */}
        <div className="mb-8">
          <h1 className="text-3xl font-black text-white tracking-tight">
            Dashboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AI-powered news monitoring and moderation
          </p>
        </div>

        {/* Backend error banner */}
        {articlesError && (
          <div className="bg-rose-900/30 border border-rose-500/40 rounded-2xl px-6 py-4 mb-6 flex items-start gap-3">
            <span className="text-rose-400 text-xl flex-shrink-0">⚠️</span>
            <div>
              <p className="text-rose-300 font-semibold text-sm">
                Backend Connection Error
              </p>
              <p className="text-rose-400/80 text-xs mt-1">{articlesError}</p>
            </div>
            <button
              onClick={refresh}
              className="ml-auto text-xs text-rose-400 hover:text-rose-200 underline flex-shrink-0"
            >
              Retry
            </button>
          </div>
        )}

        {/* ── Stats Cards ────────────────────────────────── */}
        <StatsCards stats={stats} loading={statsLoading} />

        {/* ── Charts ─────────────────────────────────────── */}
        <ChartsSection stats={stats} loading={statsLoading} />

        {/* ── Articles Table ──────────────────────────────── */}
        <ArticlesTable
          articles={articles}
          loading={articlesLoading}
          selectedArticle={selectedArticle}
          onSelect={setSelectedArticle}
          onRefresh={refresh}
        />

        {/* ── Article Details ─────────────────────────────── */}
        <ArticleDetails
          article={selectedArticle}
          onRefresh={refresh}
          addToast={addToast}
          onClose={() => setSelectedArticle(null)}
        />
      </main>

      {/* ── Toast Notifications ───────────────────────────── */}
      <Toast toasts={toasts} removeToast={removeToast} />
    </div>
  );
}

export default Dashboard;