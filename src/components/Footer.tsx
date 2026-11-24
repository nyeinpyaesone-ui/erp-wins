export default function Footer() {
  return (
    <footer className="border-t border-gray-800 bg-gray-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded bg-emerald-500/20 flex items-center justify-center">
                <span className="text-emerald-400 text-sm font-bold">E</span>
              </div>
              <span className="text-sm font-semibold text-gray-200">
                ERP Platform
              </span>
            </div>
            <p className="text-xs text-gray-500 leading-relaxed">
              Production-oriented modular business platform with clean domain
              boundaries, transactional events, and evidence-based service
              extraction. Microservices are not the default.
            </p>
          </div>

          {/* Priorities */}
          <div>
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">
              Priorities
            </h4>
            <ol className="space-y-1.5">
              {[
                "Correctness",
                "Data integrity",
                "Security",
                "Maintainability",
                "Testability",
                "Observability",
                "Performance",
                "Operational reliability",
              ].map((item, i) => (
                <li key={item} className="flex items-center gap-2 text-xs">
                  <span className="text-emerald-400 w-4">{i + 1}.</span>
                  <span className="text-gray-400">{item}</span>
                </li>
              ))}
            </ol>
          </div>

          {/* Key Rules */}
          <div>
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">
              Core Stack
            </h4>
            <ul className="space-y-1.5">
              {[
                "Python 3.12 + FastAPI",
                "SQLAlchemy 2.x Async",
                "PostgreSQL 15+ + pgvector",
                "Redis 7.x",
                "Celery 5.x",
                "Ollama (Local LLM)",
                "Docker + Compose",
                "Prometheus + Grafana",
              ].map((item) => (
                <li key={item} className="flex items-center gap-2 text-xs">
                  <span className="w-1 h-1 rounded-full bg-emerald-500" />
                  <span className="text-gray-400">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-600">
            ERP Platform Architecture Documentation
          </p>
          <div className="flex items-center gap-4">
            <span className="text-xs text-gray-600">
              Architecture: <span className="text-gray-400">Modular Monolith → Clean Boundaries → Evidence-Based Extraction</span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
