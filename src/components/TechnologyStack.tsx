interface TechItem {
  name: string;
  version: string;
  category: string;
  purpose: string;
  icon: string;
}

const technologies: TechItem[] = [
  { name: "Python", version: "3.12", category: "Runtime", purpose: "Application runtime", icon: "🐍" },
  { name: "FastAPI", version: "Latest", category: "Framework", purpose: "Async HTTP framework", icon: "⚡" },
  { name: "SQLAlchemy", version: "2.x Async", category: "ORM", purpose: "Async database ORM", icon: "🗄️" },
  { name: "asyncpg", version: "Latest", category: "Driver", purpose: "Async PostgreSQL driver", icon: "🔌" },
  { name: "PostgreSQL", version: "15+", category: "Database", purpose: "Authoritative business state", icon: "🐘" },
  { name: "pgvector", version: "Latest", category: "Extension", purpose: "Vector similarity search", icon: "📐" },
  { name: "Redis", version: "7.x", category: "Cache/Broker", purpose: "Celery broker, cache, rate limiting", icon: "🔴" },
  { name: "Celery", version: "5.x", category: "Worker", purpose: "Async task processing", icon: "🌿" },
  { name: "Ollama", version: "Latest", category: "AI", purpose: "Local LLM inference", icon: "🤖" },
  { name: "Alembic", version: "Latest", category: "Migration", purpose: "Database schema migrations", icon: "📋" },
  { name: "Docker", version: "Latest", category: "Container", purpose: "Reproducible deployments", icon: "🐳" },
  { name: "Prometheus", version: "Latest", category: "Metrics", purpose: "Metrics collection", icon: "🔥" },
  { name: "Grafana", version: "Latest", category: "Dashboard", purpose: "Metrics visualization", icon: "📊" },
  { name: "GitHub Actions", version: "—", category: "CI/CD", purpose: "Continuous integration", icon: "🔄" },
];

const categories = [...new Set(technologies.map((t) => t.category))];

export default function TechnologyStack() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Technology Stack
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Preserve supported dependency versions. Do not downgrade dependencies.
          Do not add infrastructure without a demonstrated requirement.
        </p>
      </div>

      {/* Category Sections */}
      <div className="space-y-8">
        {categories.map((category) => (
          <div key={category}>
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              {category}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {technologies
                .filter((t) => t.category === category)
                .map((tech) => (
                  <div
                    key={tech.name}
                    className="group rounded-xl border border-gray-800 bg-gray-900/30 p-4 hover:border-emerald-500/20 hover:bg-gray-900/60 transition-all"
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-xl">{tech.icon}</span>
                      <div>
                        <h4 className="text-sm font-semibold text-gray-200">
                          {tech.name}
                        </h4>
                        <span className="text-[10px] text-emerald-400">
                          v{tech.version}
                        </span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500">{tech.purpose}</p>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>

      {/* Data Flow */}
      <div className="mt-12 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <h3 className="text-lg font-semibold text-gray-200 mb-6 text-center">
          Data Flow
        </h3>
        <div className="flex flex-col items-center gap-3">
          {[
            { label: "SQLAlchemy Async", sub: "Application Layer" },
            { label: "asyncpg", sub: "Database Driver" },
            { label: "PostgreSQL 15+", sub: "Authoritative State" },
          ].map((item, i) => (
            <div key={item.label} className="flex flex-col items-center">
              <div className="px-6 py-3 rounded-lg bg-gray-800/80 border border-gray-700 text-center">
                <div className="text-sm font-semibold text-gray-200">{item.label}</div>
                <div className="text-[10px] text-gray-500">{item.sub}</div>
              </div>
              {i < 2 && <span className="text-emerald-400 text-sm my-1">↓</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
