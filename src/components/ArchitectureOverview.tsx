export default function ArchitectureOverview() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Architecture Overview
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Modular Monolith with clean domain boundaries. Microservices are not the default — 
          evidence-based service extraction guides architectural evolution.
        </p>
      </div>

      {/* Architecture Diagram */}
      <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6 sm:p-8 mb-8">
        <h3 className="text-lg font-semibold text-gray-200 mb-6 text-center">
          Layered Architecture
        </h3>
        
        <div className="space-y-4">
          {/* API Layer */}
          <div className="rounded-lg border border-sky-500/30 bg-sky-500/5 p-4">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-sky-400 text-lg">🌐</span>
              <h4 className="text-sm font-semibold text-sky-300">API Layer</h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                Thin Routes
              </span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {["router.py", "health.py", "websocket.py", "validation"].map((item) => (
                <div key={item} className="text-xs text-gray-400 bg-gray-900/50 rounded px-2 py-1.5 text-center">
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-center">
            <span className="text-emerald-400 text-lg">↓</span>
          </div>

          {/* Application Layer */}
          <div className="rounded-lg border border-purple-500/30 bg-purple-500/5 p-4">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-purple-400 text-lg">⚡</span>
              <h4 className="text-sm font-semibold text-purple-300">Application Layer</h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
                Use Cases
              </span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {["commands/", "queries/", "services/"].map((item) => (
                <div key={item} className="text-xs text-gray-400 bg-gray-900/50 rounded px-2 py-1.5 text-center">
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-center">
            <span className="text-emerald-400 text-lg">↓</span>
          </div>

          {/* Domain Layer */}
          <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 p-4">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-emerald-400 text-lg">🏛️</span>
              <h4 className="text-sm font-semibold text-emerald-300">Domain Layer</h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Business Logic
              </span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
              {["finance", "inventory", "sales", "ecommerce", "logistics", "hr", "sme"].map((item) => (
                <div key={item} className="text-xs text-gray-400 bg-gray-900/50 rounded px-2 py-1.5 text-center capitalize">
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-center">
            <span className="text-emerald-400 text-lg">↓</span>
          </div>

          {/* Infrastructure Layer */}
          <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-4">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-amber-400 text-lg">🔧</span>
              <h4 className="text-sm font-semibold text-amber-300">Infrastructure Layer</h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                External Concerns
              </span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
              {["database/", "redis/", "events/", "llm/", "vector/", "observability/"].map((item) => (
                <div key={item} className="text-xs text-gray-400 bg-gray-900/50 rounded px-2 py-1.5 text-center">
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Dependency Rules */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-5">
          <h4 className="text-sm font-semibold text-gray-200 mb-3 flex items-center gap-2">
            <span className="text-red-400">✕</span>
            Domain Must NOT Depend On
          </h4>
          <ul className="space-y-2">
            {["FastAPI", "Redis", "Celery", "Ollama", "HTTP frameworks", "Database implementations"].map((item) => (
              <li key={item} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-red-500/60" />
                <span className="text-xs text-gray-400">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-5">
          <h4 className="text-sm font-semibold text-gray-200 mb-3 flex items-center gap-2">
            <span className="text-emerald-400">✓</span>
            Domain Owns
          </h4>
          <ul className="space-y-2">
            {["Entities", "Value objects", "Domain services", "Policies", "Repository interfaces", "Domain events", "Domain exceptions"].map((item) => (
              <li key={item} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500/60" />
                <span className="text-xs text-gray-400">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
