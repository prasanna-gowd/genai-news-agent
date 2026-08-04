/**
 * StatsCards.jsx
 * Accepts stats as props from Dashboard (state is lifted up).
 * Shows animated number cards for total, pending, approved, rejected, research.
 */

const CARDS = [
  {
    key: "total_articles",
    label: "Total Articles",
    icon: "📰",
    gradient: "from-blue-600 to-indigo-700",
    glow: "shadow-blue-500/30",
  },
  {
    key: "pending",
    label: "Pending",
    icon: "⏳",
    gradient: "from-amber-500 to-orange-600",
    glow: "shadow-amber-500/30",
  },
  {
    key: "approved",
    label: "Approved",
    icon: "✅",
    gradient: "from-emerald-500 to-teal-600",
    glow: "shadow-emerald-500/30",
  },
  {
    key: "rejected",
    label: "Rejected",
    icon: "❌",
    gradient: "from-rose-500 to-pink-700",
    glow: "shadow-rose-500/30",
  },
  {
    key: "research_documents",
    label: "Research Docs",
    icon: "🤖",
    gradient: "from-violet-600 to-purple-700",
    glow: "shadow-violet-500/30",
  },
];

function StatCard({ card, value, loading }) {
  return (
    <div
      className={`relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br ${card.gradient}
        shadow-xl ${card.glow} hover:scale-105 transition-transform duration-300 cursor-default`}
    >
      {/* Background decoration */}
      <div className="absolute -right-4 -top-4 w-24 h-24 rounded-full bg-white/10 blur-xl" />
      <div className="absolute -right-2 -bottom-6 w-16 h-16 rounded-full bg-white/5" />

      <div className="relative z-10">
        <div className="flex justify-between items-start mb-4">
          <span className="text-sm font-semibold text-white/80 uppercase tracking-wider">
            {card.label}
          </span>
          <span className="text-2xl">{card.icon}</span>
        </div>

        {loading ? (
          <div className="h-10 w-16 bg-white/20 rounded-lg animate-pulse" />
        ) : (
          <p className="text-4xl font-black text-white tracking-tight">
            {value ?? 0}
          </p>
        )}
      </div>
    </div>
  );
}

function StatsCards({ stats, loading }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-4">
      {CARDS.map((card) => (
        <StatCard
          key={card.key}
          card={card}
          value={stats?.[card.key]}
          loading={loading}
        />
      ))}
    </div>
  );
}

export default StatsCards;