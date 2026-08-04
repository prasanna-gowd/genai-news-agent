/**
 * ChartsSection.jsx
 * Pure CSS/HTML charts — no external charting library required.
 * Displays: Articles by Status, Articles per Category, Articles per Day.
 */

const CATEGORY_COLORS = [
  "#6366f1", // indigo
  "#06b6d4", // cyan
  "#f59e0b", // amber
  "#10b981", // emerald
  "#f43f5e", // rose
  "#a855f7", // purple
  "#3b82f6", // blue
  "#84cc16", // lime
];

function SkeletonBar({ width = "100%", height = "1rem", className = "" }) {
  return (
    <div
      className={`bg-white/10 rounded animate-pulse ${className}`}
      style={{ width, height }}
    />
  );
}

function SectionTitle({ children }) {
  return (
    <h3 className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-4">
      {children}
    </h3>
  );
}

/* ── Status Donut-style Bars ─────────────────────────────── */
function StatusChart({ stats }) {
  const total = stats.total_articles || 1;
  const bars = [
    { label: "Pending", value: stats.pending || 0, color: "#f59e0b" },
    { label: "Approved", value: stats.approved || 0, color: "#10b981" },
    { label: "Rejected", value: stats.rejected || 0, color: "#f43f5e" },
  ];

  return (
    <div className="space-y-3">
      {bars.map((bar) => {
        const pct = total > 0 ? Math.round((bar.value / total) * 100) : 0;
        return (
          <div key={bar.label}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm text-slate-300">{bar.label}</span>
              <span className="text-sm font-bold text-white">
                {bar.value}
                <span className="text-slate-400 font-normal text-xs ml-1">
                  ({pct}%)
                </span>
              </span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{ width: `${pct}%`, backgroundColor: bar.color }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ── Category Pill Chart ─────────────────────────────────── */
function CategoryChart({ byCategory }) {
  if (!byCategory || Object.keys(byCategory).length === 0) {
    return (
      <p className="text-sm text-slate-500 italic">No category data yet.</p>
    );
  }

  const entries = Object.entries(byCategory).sort((a, b) => b[1] - a[1]);
  const max = entries[0]?.[1] || 1;

  return (
    <div className="space-y-2">
      {entries.map(([category, count], i) => {
        const pct = Math.round((count / max) * 100);
        const color = CATEGORY_COLORS[i % CATEGORY_COLORS.length];
        return (
          <div key={category}>
            <div className="flex justify-between items-center mb-1">
              <span
                className="text-sm capitalize truncate max-w-[130px]"
                style={{ color }}
              >
                {category}
              </span>
              <span className="text-sm font-bold text-white">{count}</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{ width: `${pct}%`, backgroundColor: color }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ── Articles Per Day Sparkline ──────────────────────────── */
function DayChart({ byDay }) {
  if (!byDay || byDay.length === 0) {
    return (
      <p className="text-sm text-slate-500 italic">No daily data yet.</p>
    );
  }

  const max = Math.max(...byDay.map((d) => d.count), 1);

  return (
    <div className="flex items-end gap-1 h-20">
      {byDay.map((d) => {
        const heightPct = Math.max((d.count / max) * 100, 6);
        const shortDate = d.date ? d.date.slice(5) : ""; // MM-DD
        return (
          <div
            key={d.date}
            className="flex flex-col items-center gap-1 flex-1 group"
          >
            <div className="relative w-full flex justify-center">
              {/* Tooltip */}
              <div className="absolute bottom-full mb-1 hidden group-hover:flex bg-slate-800 text-white text-xs rounded px-2 py-1 whitespace-nowrap shadow-lg z-10">
                {d.date}: {d.count} article{d.count !== 1 ? "s" : ""}
              </div>
              <div
                className="w-full rounded-t-sm transition-all duration-500"
                style={{
                  height: `${heightPct}%`,
                  minHeight: "4px",
                  background:
                    "linear-gradient(to top, #6366f1, #a78bfa)",
                }}
              />
            </div>
            <span className="text-[9px] text-slate-500 rotate-0 leading-none">
              {shortDate}
            </span>
          </div>
        );
      })}
    </div>
  );
}

/* ── Main Export ─────────────────────────────────────────── */
function ChartsSection({ stats, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 backdrop-blur-sm"
          >
            <SkeletonBar width="60%" height="0.75rem" className="mb-4" />
            <div className="space-y-3">
              <SkeletonBar height="0.5rem" />
              <SkeletonBar width="80%" height="0.5rem" />
              <SkeletonBar width="60%" height="0.5rem" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
      {/* Status Distribution */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 backdrop-blur-sm">
        <SectionTitle>Status Distribution</SectionTitle>
        <StatusChart stats={stats} />
      </div>

      {/* Articles by Category */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 backdrop-blur-sm">
        <SectionTitle>By Category</SectionTitle>
        <CategoryChart byCategory={stats.articles_by_category} />
      </div>

      {/* Articles per Day */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 backdrop-blur-sm">
        <SectionTitle>Articles per Day (last 14)</SectionTitle>
        <DayChart byDay={stats.articles_by_day} />
      </div>
    </div>
  );
}

export default ChartsSection;
