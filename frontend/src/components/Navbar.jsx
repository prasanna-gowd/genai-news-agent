/**
 * Navbar.jsx
 * Top navigation bar with branding, live status indicator,
 * and Run Pipeline button trigger (callback passed from Dashboard).
 */

function Navbar({ onRunPipeline, pipelineLoading, city, onCityChange }) {
  return (
    <header className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-white/10 shadow-xl">
      <div className="max-w-screen-2xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
        {/* ── Brand ──────────────────────────────────────────── */}
        <div className="flex items-center gap-3 flex-shrink-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-base shadow-lg">
            📰
          </div>
          <div className="hidden sm:block">
            <span className="text-white font-bold text-base leading-none">
              LocalPulse
            </span>
            <span className="text-indigo-400 font-bold text-base leading-none ml-1">
              AI
            </span>
            <p className="text-[10px] text-slate-500 leading-none mt-0.5 tracking-wide uppercase">
              News Agent
            </p>
          </div>
        </div>

        {/* ── Live badge ─────────────────────────────────────── */}
        <div className="hidden md:flex items-center gap-2 text-xs text-slate-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Live
        </div>

        {/* ── Pipeline Controls ───────────────────────────────── */}
        <div className="flex items-center gap-2 ml-auto">
          <input
            type="text"
            value={city}
            onChange={(e) => onCityChange(e.target.value)}
            placeholder="City…"
            className="hidden sm:block bg-slate-800/80 border border-white/10 text-white text-sm
              rounded-lg px-3 py-1.5 w-28 focus:outline-none focus:border-indigo-500 transition-colors
              placeholder-slate-500"
          />

          <button
            id="run-pipeline-btn"
            onClick={onRunPipeline}
            disabled={pipelineLoading}
            className="flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-violet-600
              hover:from-indigo-500 hover:to-violet-500 disabled:opacity-60
              text-white text-sm font-semibold px-4 py-2 rounded-xl shadow-lg
              shadow-indigo-900/40 transition-all active:scale-95"
          >
            {pipelineLoading ? (
              <>
                <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Running…
              </>
            ) : (
              <>
                <span>⚡</span>
                Run Pipeline
              </>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
