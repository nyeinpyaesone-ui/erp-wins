export default function ArchitectureHero() {
  return (
    <div id="overview" className="relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-gray-950 via-gray-900 to-emerald-950/20" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-emerald-900/20 via-transparent to-transparent" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/80 border border-gray-700 mb-8">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-gray-300">Modular Monolith • Clean Architecture • Production Ready</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6">
            <span className="text-gray-100">ERP </span>
            <span className="text-emerald-400">Platform</span>
          </h1>

          <p className="text-lg sm:text-xl text-gray-400 max-w-3xl mx-auto mb-4">
            Production-oriented modular business platform with clean domain boundaries,
            transactional events, and evidence-based service extraction.
          </p>
          <p className="text-sm text-gray-500 max-w-2xl mx-auto mb-10">
            Python 3.12 • FastAPI • SQLAlchemy 2.x Async • PostgreSQL 15+ • Redis 7.x • Celery 5.x • Ollama
          </p>

          {/* Architecture Flow */}
          <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-4 mb-12">
            {["API", "Application", "Domain", "Infrastructure"].map((layer, i) => (
              <div key={layer} className="flex items-center gap-2 sm:gap-4">
                <div className="px-4 py-2 rounded-lg bg-gray-800/80 border border-gray-700 text-sm text-gray-200">
                  {layer}
                </div>
                {i < 3 && <span className="text-emerald-400 text-lg">↓</span>}
              </div>
            ))}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto">
            {[
              { label: "Domains", value: "13" },
              { label: "Stages Complete", value: "3/7" },
              { label: "System Records", value: "129+" },
              { label: "Priority", value: "Correctness" },
            ].map((stat) => (
              <div
                key={stat.label}
                className="px-4 py-3 rounded-lg bg-gray-800/50 border border-gray-700/50"
              >
                <div className="text-lg font-bold text-emerald-400">{stat.value}</div>
                <div className="text-xs text-gray-500">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-gray-950 to-transparent" />
    </div>
  );
}
