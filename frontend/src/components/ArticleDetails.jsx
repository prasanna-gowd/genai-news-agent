/**
 * ArticleDetails.jsx
 * Slide-in right-panel. Shows full article metadata with graceful
 * "Not available" fallbacks. Action buttons have per-button loading state
 * and fire toast notifications + auto-refresh on success.
 */

import { useState } from "react";
import {
  approveArticle,
  rejectArticle,
  deleteArticle,
} from "../services/api";

const STATUS_STYLES = {
  APPROVED: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40",
  REJECTED: "bg-rose-500/20 text-rose-400 border border-rose-500/40",
  PENDING_APPROVAL:
    "bg-amber-500/20 text-amber-400 border border-amber-500/40",
};

function StatusBadge({ status }) {
  const cls = STATUS_STYLES[status] || "bg-slate-500/20 text-slate-400";
  const label =
    status === "PENDING_APPROVAL" ? "Pending Approval" : (status ?? "Unknown");
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${cls}`}
    >
      {label}
    </span>
  );
}

function MetaItem({ label, children }) {
  return (
    <div>
      <dt className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
        {label}
      </dt>
      <dd className="text-sm text-slate-200">{children}</dd>
    </div>
  );
}

function Section({ title, children, accent = "border-indigo-500" }) {
  return (
    <div className={`border-l-2 ${accent} pl-4`}>
      <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">
        {title}
      </h3>
      {children}
    </div>
  );
}

function NotAvailable({ label }) {
  return (
    <p className="text-sm text-slate-500 italic">
      {label} not available. Run the AI pipeline to generate this data.
    </p>
  );
}

function ActionButton({ label, onClick, loading, variant = "default" }) {
  const variants = {
    approve:
      "bg-emerald-600 hover:bg-emerald-500 border-emerald-500 shadow-emerald-900/40",
    reject:
      "bg-amber-600 hover:bg-amber-500 border-amber-500 shadow-amber-900/40",
    delete:
      "bg-rose-700 hover:bg-rose-600 border-rose-600 shadow-rose-900/40",
    default: "bg-slate-700 hover:bg-slate-600 border-slate-600",
  };

  return (
    <button
      onClick={onClick}
      disabled={loading}
      className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white
        border transition-all shadow-lg ${variants[variant]}
        disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      {loading && (
        <span className="inline-block w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
      )}
      {label}
    </button>
  );
}

function ArticleDetails({ article, onRefresh, addToast, onClose }) {
  const [actionLoading, setActionLoading] = useState(null); // "approve" | "reject" | "delete"

  if (!article) {
    return (
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-10 mt-8 text-center backdrop-blur-sm">
        <div className="text-5xl mb-4">📄</div>
        <h2 className="text-xl font-bold text-white mb-2">
          No Article Selected
        </h2>
        <p className="text-slate-400 text-sm">
          Click any row in the table above to view its full details.
        </p>
      </div>
    );
  }

  async function handleApprove() {
    setActionLoading("approve");
    try {
      await approveArticle(article.hash);
      addToast?.("Article approved successfully.", "success");
      onRefresh?.();
    } catch (err) {
      addToast?.(
        `Approve failed: ${err.response?.data?.detail || err.message}`,
        "error"
      );
    } finally {
      setActionLoading(null);
    }
  }

  async function handleReject() {
    setActionLoading("reject");
    try {
      await rejectArticle(article.hash);
      addToast?.("Article rejected.", "warning");
      onRefresh?.();
    } catch (err) {
      addToast?.(
        `Reject failed: ${err.response?.data?.detail || err.message}`,
        "error"
      );
    } finally {
      setActionLoading(null);
    }
  }

  async function handleDelete() {
    if (!window.confirm(`Delete article "${article.title}"? This cannot be undone.`))
      return;

    setActionLoading("delete");
    try {
      await deleteArticle(article.hash);
      addToast?.("Article deleted.", "info");
      onClose?.();
      onRefresh?.();
    } catch (err) {
      addToast?.(
        `Delete failed: ${err.response?.data?.detail || err.message}`,
        "error"
      );
    } finally {
      setActionLoading(null);
    }
  }

  const published = article.published
    ? new Date(article.published).toLocaleString("en-IN", {
        dateStyle: "long",
        timeStyle: "short",
      })
    : null;

  return (
    <div className="bg-slate-800/60 border border-white/10 rounded-2xl mt-8 backdrop-blur-sm overflow-hidden">
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="bg-gradient-to-r from-indigo-900/60 to-slate-800/60 px-6 py-5 border-b border-white/10">
        <div className="flex justify-between items-start gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 mb-2 flex-wrap">
              <StatusBadge status={article.status} />
              {article.importance_score != null && (
                <span className="text-xs text-slate-400 bg-slate-700/60 border border-white/10 rounded-full px-2.5 py-0.5">
                  Score: {article.importance_score}
                </span>
              )}
            </div>
            <h1 className="text-xl font-bold text-white leading-snug">
              {article.title}
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              {[article.city, article.category]
                .filter(Boolean)
                .join(" • ")}
            </p>
          </div>

          {onClose && (
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white transition-colors text-xl leading-none flex-shrink-0"
              aria-label="Close"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* ── Action Buttons ───────────────────────────────────── */}
      <div className="flex flex-wrap gap-3 px-6 py-4 border-b border-white/10">
        <ActionButton
          label="Approve"
          onClick={handleApprove}
          loading={actionLoading === "approve"}
          variant="approve"
        />
        <ActionButton
          label="Reject"
          onClick={handleReject}
          loading={actionLoading === "reject"}
          variant="reject"
        />
        <ActionButton
          label="Delete"
          onClick={handleDelete}
          loading={actionLoading === "delete"}
          variant="delete"
        />
      </div>

      {/* ── Meta Info ────────────────────────────────────────── */}
      <div className="px-6 py-5 border-b border-white/10">
        <dl className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <MetaItem label="Published">
            {published ?? <span className="text-slate-500 italic">Unknown</span>}
          </MetaItem>
          <MetaItem label="Source">{article.source || "—"}</MetaItem>
          <MetaItem label="Language">{article.language || "—"}</MetaItem>
          <MetaItem label="Hash">
            <code className="text-xs text-indigo-400 break-all">
              {article.hash?.slice(0, 12)}…
            </code>
          </MetaItem>
        </dl>

        {article.url && (
          <div className="mt-4">
            <dt className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
              URL
            </dt>
            <a
              href={article.url}
              target="_blank"
              rel="noreferrer"
              className="text-sm text-indigo-400 hover:text-indigo-300 underline underline-offset-2 break-all"
            >
              {article.url}
            </a>
          </div>
        )}
      </div>

      {/* ── Content Sections ─────────────────────────────────── */}
      <div className="px-6 py-5 space-y-6">
        {/* Original Article */}
        <Section title="Original Article" accent="border-cyan-500">
          {article.scraped_article?.text ? (
            <p className="text-sm text-slate-300 whitespace-pre-wrap leading-relaxed max-h-56 overflow-y-auto pr-1
              scrollbar-thin scrollbar-thumb-white/10">
              {article.scraped_article.text}
            </p>
          ) : article.description ? (
            <p className="text-sm text-slate-300 leading-relaxed">
              {article.description}
            </p>
          ) : (
            <NotAvailable label="Scraped article text" />
          )}
        </Section>

        {/* Caption */}
        <Section title="Caption" accent="border-blue-500">
          {article.caption ? (
            <div className="bg-blue-900/20 border border-blue-500/20 rounded-xl p-4 text-sm text-slate-200 leading-relaxed">
              {article.caption}
            </div>
          ) : (
            <NotAvailable label="AI-generated caption" />
          )}
        </Section>

        {/* Image Prompt */}
        <Section title="Image Prompt" accent="border-violet-500">
          {article.image_prompt ? (
            <div className="bg-violet-900/20 border border-violet-500/20 rounded-xl p-4 text-sm text-slate-200 leading-relaxed font-mono">
              {article.image_prompt}
            </div>
          ) : (
            <NotAvailable label="Image prompt" />
          )}
        </Section>

        {/* AI Research */}
        <Section title="AI Research" accent="border-emerald-500">
          {article.research ? (
            <pre className="bg-slate-900/60 border border-white/10 rounded-xl p-4 text-xs text-slate-300
              overflow-auto max-h-72 whitespace-pre-wrap font-mono leading-relaxed">
              {typeof article.research === "string"
                ? article.research
                : JSON.stringify(article.research, null, 2)}
            </pre>
          ) : (
            <NotAvailable label="AI research data" />
          )}
        </Section>
      </div>
    </div>
  );
}

export default ArticleDetails;