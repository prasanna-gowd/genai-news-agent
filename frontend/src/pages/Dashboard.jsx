/**
 * Dashboard.jsx
 * Central dashboard orchestrator.
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

  // ============================================================
  // STATE
  // ============================================================

  const [articles, setArticles] = useState([]);
  const [articlesLoading, setArticlesLoading] = useState(true);
  const [articlesError, setArticlesError] = useState("");

  const [stats, setStats] = useState(null);
  const [statsLoading, setStatsLoading] = useState(true);

  const [selectedArticle, setSelectedArticle] = useState(null);

  const [pipelineLoading, setPipelineLoading] = useState(false);

  const [city, setCity] = useState("Anantapur");

  const {
    toasts,
    addToast,
    removeToast,
  } = useToast();


  // ============================================================
  // LOAD ARTICLES
  // ============================================================

  const loadArticles = useCallback(async () => {

    try {

      setArticlesLoading(true);
      setArticlesError("");

      const data = await fetchAllArticles();

      console.log("Articles API response:", data);

      const articleList = Array.isArray(data?.articles)
        ? data.articles
        : [];

      setArticles(articleList);


      // Keep selected article synchronized
      setSelectedArticle((previous) => {

        if (!previous) {
          return null;
        }

        const updatedArticle = articleList.find(
          (article) => article.hash === previous.hash
        );

        return updatedArticle ?? previous;

      });

    } catch (error) {

      console.error(
        "Failed to load articles:",
        error
      );

      const message =
        error?.response?.data?.detail ||
        error?.response?.data?.error ||
        error?.message ||
        "Could not connect to the backend.";

      setArticlesError(message);

    } finally {

      setArticlesLoading(false);

    }

  }, []);


  // ============================================================
  // LOAD STATS
  // ============================================================

  const loadStats = useCallback(async () => {

    try {

      setStatsLoading(true);

      const data = await fetchStats();

      console.log("Stats API response:", data);

      setStats(data ?? {
        total_articles: 0,
        pending: 0,
        approved: 0,
        rejected: 0,
        research_documents: 0,
        articles_by_category: {},
        articles_by_day: [],
      });

    } catch (error) {

      console.error(
        "Failed to load stats:",
        error
      );

      // Keep dashboard usable even if stats fail
      setStats({
        total_articles: 0,
        pending: 0,
        approved: 0,
        rejected: 0,
        research_documents: 0,
        articles_by_category: {},
        articles_by_day: [],
      });

    } finally {

      setStatsLoading(false);

    }

  }, []);


  // ============================================================
  // REFRESH
  // ============================================================

  const refresh = useCallback(async () => {

    await Promise.all([
      loadArticles(),
      loadStats(),
    ]);

  }, [
    loadArticles,
    loadStats,
  ]);


  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {

    refresh();

  }, [refresh]);


  // ============================================================
  // AUTO REFRESH
  // ============================================================

  useEffect(() => {

    const interval = setInterval(
      refresh,
      60_000
    );

    return () => {
      clearInterval(interval);
    };

  }, [refresh]);


  // ============================================================
  // RUN PIPELINE
  // ============================================================

  async function handleRunPipeline() {

    if (pipelineLoading) {
      return;
    }

    setPipelineLoading(true);

    addToast(
      `Running pipeline for "${city}"…`,
      "info"
    );

    try {

      const result = await runPipeline(city);

      console.log(
        "Pipeline response:",
        result
      );

      addToast(
        "Pipeline completed successfully! Refreshing data…",
        "success"
      );

      await refresh();

    } catch (error) {

      console.error(
        "Pipeline failed:",
        error
      );

      const message =
        error?.response?.data?.detail ||
        error?.response?.data?.error ||
        error?.message ||
        "Pipeline execution failed.";

      addToast(
        `Pipeline failed: ${message}`,
        "error"
      );

    } finally {

      setPipelineLoading(false);

    }

  }


  // ============================================================
  // RENDER
  // ============================================================

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      {/* ======================================================
          NAVBAR
      ====================================================== */}

      <Navbar
        onRunPipeline={handleRunPipeline}
        pipelineLoading={pipelineLoading}
        city={city}
        onCityChange={setCity}
      />


      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="max-w-screen-2xl mx-auto px-4 sm:px-6 py-8">


        {/* ====================================================
            PAGE TITLE
        ==================================================== */}

        <div className="mb-8">

          <h1 className="text-3xl font-black text-white tracking-tight">
            Dashboard
          </h1>

          <p className="text-slate-400 text-sm mt-1">
            AI-powered news monitoring and moderation
          </p>

        </div>


        {/* ====================================================
            BACKEND ERROR
        ==================================================== */}

        {articlesError && (

          <div className="bg-rose-900/30 border border-rose-500/40 rounded-2xl px-6 py-4 mb-6 flex items-start gap-3">

            <span className="text-rose-400 text-xl flex-shrink-0">
              ⚠️
            </span>

            <div>

              <p className="text-rose-300 font-semibold text-sm">
                Backend Connection Error
              </p>

              <p className="text-rose-400/80 text-xs mt-1">
                {articlesError}
              </p>

            </div>

            <button
              onClick={refresh}
              className="ml-auto text-xs text-rose-400 hover:text-rose-200 underline flex-shrink-0"
            >
              Retry
            </button>

          </div>

        )}


        {/* ====================================================
            STATS
        ==================================================== */}

        <StatsCards
          stats={stats}
          loading={statsLoading}
        />


        {/* ====================================================
            CHARTS
        ==================================================== */}

        <ChartsSection
          stats={stats}
          loading={statsLoading}
        />


        {/* ====================================================
            ARTICLES
        ==================================================== */}

        <ArticlesTable
          articles={articles}
          loading={articlesLoading}
          selectedArticle={selectedArticle}
          onSelect={setSelectedArticle}
          onRefresh={refresh}
        />


        {/* ====================================================
            ARTICLE DETAILS
        ==================================================== */}

        <ArticleDetails
          article={selectedArticle}
          onRefresh={refresh}
          addToast={addToast}
          onClose={() => setSelectedArticle(null)}
        />

      </main>


      {/* ======================================================
          TOASTS
      ====================================================== */}

      <Toast
        toasts={toasts}
        removeToast={removeToast}
      />

    </div>

  );

}


export default Dashboard;