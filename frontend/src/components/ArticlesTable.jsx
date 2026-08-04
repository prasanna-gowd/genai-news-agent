/**
 * ArticlesTable.jsx
 * Features: search, status filter, client-side pagination, skeleton loader,
 * auto-refresh via onRefresh prop, row selection via onSelect prop.
 */

import { useEffect, useState, useMemo } from "react";

const PAGE_SIZE = 10;

const STATUS_OPTIONS = [
  { label: "All", value: "ALL" },
  { label: "Pending", value: "PENDING_APPROVAL" },
  { label: "Approved", value: "APPROVED" },
  { label: "Rejected", value: "REJECTED" },
];

const STATUS_STYLES = {
  APPROVED: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
  REJECTED: "bg-rose-500/20 text-rose-400 border border-rose-500/30",
  PENDING_APPROVAL:
    "bg-amber-500/20 text-amber-400 border border-amber-500/30",
};

function StatusBadge({ status }) {
  const cls = STATUS_STYLES[status] || "bg-slate-500/20 text-slate-400";
  const label =
    status === "PENDING_APPROVAL" ? "Pending" : (status ?? "Unknown");
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${cls}`}
    >
      {label}
    </span>
  );
}

function SkeletonRow() {
  return (
    <tr className="border-t border-white/5 animate-pulse">
      {[1, 2, 3, 4, 5].map((i) => (
        <td key={i} className="px-4 py-3">
          <div className="h-4 bg-white/10 rounded" />
        </td>
      ))}
    </tr>
  );
}

function ArticlesTable({ articles, loading, selectedArticle, onSelect, onRefresh }) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [page, setPage] = useState(1);

  // Reset to page 1 whenever filter/search changes
  useEffect(() => {
    setPage(1);
  }, [search, statusFilter]);

  const filtered = useMemo(() => {
    if (!articles) return [];
    return articles.filter((a) => {
      const matchSearch =
        !search ||
        (a.title || "").toLowerCase().includes(search.toLowerCase()) ||
        (a.city || "").toLowerCase().includes(search.toLowerCase()) ||
        (a.category || "").toLowerCase().includes(search.toLowerCase());

      const matchStatus =
        statusFilter === "ALL" || a.status === statusFilter;

      return matchSearch && matchStatus;
    });
  }, [articles, search, statusFilter]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(page, totalPages);
  const pageSlice = filtered.slice(
    (safePage - 1) * PAGE_SIZE,
    safePage * PAGE_SIZE
  );

  // Count per status for filter badges
  const counts = useMemo(() => {
    if (!articles) return {};
    return articles.reduce((acc, a) => {
      acc[a.status] = (acc[a.status] || 0) + 1;
      return acc;
    }, {});
  }, [articles]);

  return (
    <div className="bg-slate-800/60 border border-white/10 rounded-2xl backdrop-blur-sm mt-8 overflow-hidden">
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 px-6 py-5 border-b border-white/10">
        <div>
          <h2 className="text-lg font-bold text-white">Articles</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            {filtered.length} of {articles?.length ?? 0} total
          </p>
        </div>

        <button
          onClick={onRefresh}
          disabled={loading}
          className="flex items-center gap-2 text-sm bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50
            text-white px-4 py-2 rounded-xl transition-colors font-medium"
        >
          <span className={loading ? "animate-spin" : ""}>↻</span>
          Refresh
        </button>
      </div>

      {/* ── Search + Filter ───────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row gap-3 px-6 py-4 border-b border-white/10">
        {/* Search */}
        <div className="relative flex-1">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">
            🔍
          </span>
          <input
            id="article-search"
            type="text"
            placeholder="Search by title, city or category…"
            className="w-full bg-slate-900/60 border border-white/10 text-white placeholder-slate-500
              rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500 transition-colors"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Status filter */}
        <div className="flex gap-2 flex-wrap">
          {STATUS_OPTIONS.map((opt) => {
            const active = statusFilter === opt.value;
            const count =
              opt.value === "ALL"
                ? articles?.length ?? 0
                : counts[opt.value] ?? 0;

            return (
              <button
                key={opt.value}
                onClick={() => setStatusFilter(opt.value)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold
                  border transition-all ${
                    active
                      ? "bg-indigo-600 border-indigo-500 text-white"
                      : "bg-transparent border-white/10 text-slate-400 hover:border-white/30 hover:text-white"
                  }`}
              >
                {opt.label}
                <span
                  className={`text-[10px] rounded-full px-1.5 py-0.5 ${
                    active ? "bg-white/20 text-white" : "bg-white/10"
                  }`}
                >
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Table ────────────────────────────────────────────── */}
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-xs uppercase tracking-wider text-slate-500 border-b border-white/5">
              <th className="text-left px-4 py-3 font-semibold">Title</th>
              <th className="text-left px-4 py-3 font-semibold">City</th>
              <th className="text-left px-4 py-3 font-semibold">Category</th>
              <th className="text-left px-4 py-3 font-semibold">Status</th>
              <th className="text-left px-4 py-3 font-semibold">Published</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
              Array.from({ length: 6 }).map((_, i) => (
                <SkeletonRow key={i} />
              ))
            ) : pageSlice.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="text-center py-16 text-slate-500 italic"
                >
                  {search || statusFilter !== "ALL"
                    ? "No articles match your filters."
                    : "No articles found. Run the pipeline to fetch news."}
                </td>
              </tr>
            ) : (
              pageSlice.map((article) => {
                const isSelected =
                  selectedArticle?.hash === article.hash;

                return (
                  <tr
                    key={article.hash}
                    onClick={() => onSelect(article)}
                    className={`border-t border-white/5 cursor-pointer transition-colors
                      ${
                        isSelected
                          ? "bg-indigo-900/40 border-l-2 border-l-indigo-500"
                          : "hover:bg-white/5"
                      }`}
                  >
                    <td className="px-4 py-3 max-w-xs">
                      <div className="font-medium text-white truncate">
                        {article.title || "Untitled"}
                      </div>
                      {article.url && (
                        <div className="text-xs text-indigo-400 truncate mt-0.5">
                          {article.url}
                        </div>
                      )}
                    </td>

                    <td className="px-4 py-3 text-slate-300 whitespace-nowrap">
                      {article.city || "—"}
                    </td>

                    <td className="px-4 py-3 text-slate-300 whitespace-nowrap capitalize">
                      {article.category || "—"}
                    </td>

                    <td className="px-4 py-3">
                      <StatusBadge status={article.status} />
                    </td>

                    <td className="px-4 py-3 text-slate-400 whitespace-nowrap text-xs">
                      {article.published
                        ? new Date(article.published).toLocaleDateString(
                            "en-IN",
                            {
                              day: "2-digit",
                              month: "short",
                              year: "numeric",
                            }
                          )
                        : "—"}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* ── Pagination ───────────────────────────────────────── */}
      {!loading && totalPages > 1 && (
        <div className="flex justify-between items-center px-6 py-4 border-t border-white/10">
          <p className="text-xs text-slate-500">
            Page {safePage} of {totalPages}
          </p>

          <div className="flex gap-1">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={safePage === 1}
              className="px-3 py-1.5 rounded-lg border border-white/10 text-slate-400 text-xs
                hover:border-indigo-500 hover:text-white disabled:opacity-30 transition-colors"
            >
              ← Prev
            </button>

            {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
              let p;
              if (totalPages <= 7) {
                p = i + 1;
              } else if (safePage <= 4) {
                p = i + 1;
              } else if (safePage >= totalPages - 3) {
                p = totalPages - 6 + i;
              } else {
                p = safePage - 3 + i;
              }
              return (
                <button
                  key={p}
                  onClick={() => setPage(p)}
                  className={`w-8 h-8 rounded-lg text-xs font-semibold transition-colors
                    ${
                      p === safePage
                        ? "bg-indigo-600 text-white"
                        : "border border-white/10 text-slate-400 hover:border-indigo-500 hover:text-white"
                    }`}
                >
                  {p}
                </button>
              );
            })}

            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={safePage === totalPages}
              className="px-3 py-1.5 rounded-lg border border-white/10 text-slate-400 text-xs
                hover:border-indigo-500 hover:text-white disabled:opacity-30 transition-colors"
            >
              Next →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ArticlesTable;