import { useState } from "react";

interface Stage {
  id: number;
  name: string;
  subtitle: string;
  icon: string;
  color: string;
  items: string[];
}

const stages: Stage[] = [
  {
    id: 1,
    name: "Foundation",
    subtitle: "Core infrastructure and tooling",
    icon: "🏗️",
    color: "emerald",
    items: [
      "Repository setup",
      "Configuration management",
      "FastAPI application",
      "PostgreSQL database",
      "Redis cache/broker",
      "Alembic migrations",
      "Docker containers",
      "CI/CD pipeline",
      "Health checks (live, ready, startup)",
    ],
  },
  {
    id: 2,
    name: "Core Business",
    subtitle: "Essential business entities",
    icon: "🏛️",
    color: "blue",
    items: [
      "Users & authentication",
      "Organizations",
      "Branches",
      "Roles & permissions",
      "Products",
      "Customers",
      "Suppliers",
      "Inventory management",
    ],
  },
  {
    id: 3,
    name: "Transactions",
    subtitle: "Business operations",
    icon: "💳",
    color: "amber",
    items: [
      "Sales orders",
      "Purchase orders",
      "Payments",
      "Receivables",
      "Payables",
      "Accounting basics",
      "Daily closing",
    ],
  },
  {
    id: 4,
    name: "Event Runtime",
    subtitle: "Asynchronous processing",
    icon: "📡",
    color: "purple",
    items: [
      "Domain events",
      "Transactional outbox",
      "Event dispatcher",
      "Celery workers",
      "Idempotency",
      "Retry with backoff",
      "Dead-letter handling",
    ],
  },
  {
    id: 5,
    name: "Marketplace",
    subtitle: "E-commerce capabilities",
    icon: "🛍️",
    color: "cyan",
    items: [
      "Marketplace platform",
      "Orders & shipments",
      "Logistics integration",
      "Reviews",
      "Messaging",
    ],
  },
  {
    id: 6,
    name: "AI",
    subtitle: "Intelligent automation",
    icon: "🤖",
    color: "pink",
    items: [
      "AI Gateway",
      "Ollama integration",
      "RAG pipeline",
      "Decision Engine",
      "Agent Runtime",
      "Policy Engine",
      "Human Approval workflows",
    ],
  },
  {
    id: 7,
    name: "Production Hardening",
    subtitle: "Operational readiness",
    icon: "🛡️",
    color: "orange",
    items: [
      "Prometheus metrics",
      "Grafana dashboards",
      "Structured logging",
      "Security hardening",
      "Backup & restore",
      "Performance testing",
      "Failure testing",
      "Deployment procedures",
      "Rollback procedures",
    ],
  },
];

const colorMap: Record<string, { border: string; bg: string; text: string; dot: string; line: string }> = {
  emerald: { border: "border-emerald-500/30", bg: "bg-emerald-500/5", text: "text-emerald-400", dot: "bg-emerald-400", line: "bg-emerald-500/20" },
  blue: { border: "border-blue-500/30", bg: "bg-blue-500/5", text: "text-blue-400", dot: "bg-blue-400", line: "bg-blue-500/20" },
  amber: { border: "border-amber-500/30", bg: "bg-amber-500/5", text: "text-amber-400", dot: "bg-amber-400", line: "bg-amber-500/20" },
  purple: { border: "border-purple-500/30", bg: "bg-purple-500/5", text: "text-purple-400", dot: "bg-purple-400", line: "bg-purple-500/20" },
  cyan: { border: "border-cyan-500/30", bg: "bg-cyan-500/5", text: "text-cyan-400", dot: "bg-cyan-400", line: "bg-cyan-500/20" },
  pink: { border: "border-pink-500/30", bg: "bg-pink-500/5", text: "text-pink-400", dot: "bg-pink-400", line: "bg-pink-500/20" },
  orange: { border: "border-orange-500/30", bg: "bg-orange-500/5", text: "text-orange-400", dot: "bg-orange-400", line: "bg-orange-500/20" },
};

export default function ImplementationStages() {
  const [activeStage, setActiveStage] = useState(0);
  const stage = stages[activeStage];
  const colors = colorMap[stage.color];

  // Stage 1, 2, and 3 are 100% complete
  const getStageProgress = (stageId: number): number => {
    if (stageId === 1 || stageId === 2 || stageId === 3) return 100;
    if (stageId < activeStage + 1) return 100;
    if (stageId === activeStage + 1) return 50;
    return 0;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Implementation Stages
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Seven stages of progressive capability building. Each stage builds on the previous,
          ensuring a solid foundation before adding complexity.
        </p>
      </div>

      {/* Stage Timeline */}
      <div className="flex flex-wrap justify-center gap-2 mb-10">
        {stages.map((s, i) => {
          const c = colorMap[s.color];
          return (
            <button
              key={s.id}
              onClick={() => setActiveStage(i)}
              className={`px-3 py-2 rounded-lg text-xs transition-all flex items-center gap-2 ${
                activeStage === i
                  ? `${c.bg} ${c.border} border ${c.text}`
                  : "bg-gray-900/50 border border-gray-800 text-gray-400 hover:border-gray-700"
              }`}
            >
              <span>{s.icon}</span>
              <span className="hidden sm:inline">{s.name}</span>
              <span className="sm:hidden">S{s.id}</span>
            </button>
          );
        })}
      </div>

      {/* Stage Detail */}
      <div className={`rounded-xl border ${colors.border} ${colors.bg} p-6 sm:p-8`}>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 rounded-xl bg-gray-800 flex items-center justify-center text-2xl">
            {stage.icon}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className={`text-xs px-2 py-0.5 rounded ${colors.text} bg-gray-800`}>
                Stage {stage.id}
              </span>
            </div>
            <h3 className={`text-xl font-bold ${colors.text} mt-1`}>{stage.name}</h3>
            <p className="text-xs text-gray-500">{stage.subtitle}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {stage.items.map((item, i) => (
            <div
              key={item}
              className="flex items-center gap-3 p-3 rounded-lg bg-gray-950/50 border border-gray-800/50"
            >
              <span className={`w-5 h-5 rounded-full ${colors.dot} flex items-center justify-center text-[10px] text-gray-900 font-bold`}>
                {i + 1}
              </span>
              <span className="text-xs text-gray-300">{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Progress Overview */}
      <div className="mt-8 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <h4 className="text-sm font-semibold text-gray-200 mb-4">
          📈 Implementation Progress
        </h4>
        <div className="space-y-3">
          {stages.map((s) => {
            const c = colorMap[s.color];
            const progress = getStageProgress(s.id);
            return (
              <div key={s.id} className="flex items-center gap-3">
                <span className="text-xs text-gray-500 w-6">S{s.id}</span>
                <span className="text-xs text-gray-300 w-32 truncate">{s.name}</span>
                <div className="flex-1 h-2 rounded-full bg-gray-800 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${c.dot} transition-all duration-500`}
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500 w-10 text-right">{progress}%</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Stage 1 Completion Details */}
      {activeStage === 0 && (
        <div className="mt-8 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">✅</span>
            <div>
              <h4 className="text-lg font-bold text-emerald-400">Stage 1 — Foundation Complete</h4>
              <p className="text-xs text-gray-400">All core infrastructure components implemented and verified</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Created Files</h5>
              <div className="space-y-1.5">
                {[
                  "pyproject.toml",
                  ".env.example",
                  "app/__init__.py",
                  "app/config.py",
                  "app/main.py",
                  "app/lifespan.py",
                  "app/api/__init__.py",
                  "app/api/router.py",
                  "app/api/health.py",
                  "app/api/websocket.py",
                  "app/infrastructure/database/engine.py",
                  "app/infrastructure/database/base.py",
                  "app/infrastructure/redis/client.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-emerald-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Infrastructure</h5>
              <div className="space-y-1.5">
                {[
                  "alembic.ini",
                  "migrations/env.py",
                  "migrations/script.py.mako",
                  "Dockerfile",
                  "docker-compose.yml",
                  ".dockerignore",
                  ".github/workflows/ci.yml",
                  "deploy/prometheus.yml",
                  "workers/celery_app.py",
                  "tests/conftest.py",
                  "tests/api/test_health.py",
                  "tests/unit/test_config.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-emerald-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-4">
            <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Key Features Implemented</h5>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {[
                "Pydantic Settings with validation",
                "Async SQLAlchemy engine with bounded pool",
                "Redis client with health checks",
                "FastAPI lifespan management",
                "Health endpoints (live, ready, startup)",
                "WebSocket notification transport",
                "Alembic async migrations",
                "Multi-stage Docker build",
                "Non-root container security",
                "Docker Compose with all services",
                "GitHub Actions CI pipeline",
                "Prometheus + Grafana observability",
                "Celery worker and beat scheduler",
                "Comprehensive test suite",
                "Structured logging",
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2 text-xs p-2 rounded bg-gray-950/50">
                  <span className="text-emerald-400">✓</span>
                  <span className="text-gray-400">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stage 2 Completion Details */}
      {activeStage === 1 && (
        <div className="mt-8 rounded-xl border border-blue-500/30 bg-blue-500/5 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">✅</span>
            <div>
              <h4 className="text-lg font-bold text-blue-400">Stage 2 — Core Business Complete</h4>
              <p className="text-xs text-gray-400">All core business entities and authentication implemented</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Created Files</h5>
              <div className="space-y-1.5">
                {[
                  "pyproject.toml",
                  ".env.example",
                  "app/__init__.py",
                  "app/config.py",
                  "app/main.py",
                  "app/lifespan.py",
                  "app/api/__init__.py",
                  "app/api/router.py",
                  "app/api/health.py",
                  "app/api/websocket.py",
                  "app/infrastructure/database/engine.py",
                  "app/infrastructure/database/base.py",
                  "app/infrastructure/redis/client.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-emerald-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Infrastructure</h5>
              <div className="space-y-1.5">
                {[
                  "alembic.ini",
                  "migrations/env.py",
                  "migrations/script.py.mako",
                  "Dockerfile",
                  "docker-compose.yml",
                  ".dockerignore",
                  ".github/workflows/ci.yml",
                  "deploy/prometheus.yml",
                  "workers/celery_app.py",
                  "tests/conftest.py",
                  "tests/api/test_health.py",
                  "tests/unit/test_config.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-emerald-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-4">
            <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Key Features Implemented</h5>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {[
                "Pydantic Settings with validation",
                "Async SQLAlchemy engine with bounded pool",
                "Redis client with health checks",
                "FastAPI lifespan management",
                "Health endpoints (live, ready, startup)",
                "WebSocket notification transport",
                "Alembic async migrations",
                "Multi-stage Docker build",
                "Non-root container security",
                "Docker Compose with all services",
                "GitHub Actions CI pipeline",
                "Prometheus + Grafana observability",
                "Celery worker and beat scheduler",
                "Comprehensive test suite",
                "Structured logging",
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2 text-xs p-2 rounded bg-gray-950/50">
                  <span className="text-emerald-400">✓</span>
                  <span className="text-gray-400">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stage 2 Completion Details */}
      {activeStage === 1 && (
        <div className="mt-8 rounded-xl border border-blue-500/30 bg-blue-500/5 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">✅</span>
            <div>
              <h4 className="text-lg font-bold text-blue-400">Stage 2 — Core Business Complete</h4>
              <p className="text-xs text-gray-400">All core business entities and authentication implemented</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Domain Entities</h5>
              <div className="space-y-1.5">
                {[
                  "app/domain/users/entities.py",
                  "app/domain/organizations/entities.py",
                  "app/domain/branches/entities.py",
                  "app/domain/roles/entities.py",
                  "app/domain/products/entities.py",
                  "app/domain/customers/entities.py",
                  "app/domain/suppliers/entities.py",
                  "app/domain/inventory/entities.py",
                  "app/domain/exceptions.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-blue-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Infrastructure</h5>
              <div className="space-y-1.5">
                {[
                  "app/infrastructure/database/models/user.py",
                  "app/infrastructure/database/models/organization.py",
                  "app/infrastructure/database/models/branch.py",
                  "app/infrastructure/database/models/role.py",
                  "app/infrastructure/database/models/product.py",
                  "app/infrastructure/database/models/customer.py",
                  "app/infrastructure/database/models/supplier.py",
                  "app/infrastructure/database/models/inventory.py",
                  "app/infrastructure/repositories/user_repository.py",
                  "app/infrastructure/auth/security.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-blue-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-4">
            <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Key Features Implemented</h5>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {[
                "User authentication (JWT)",
                "Password hashing (bcrypt)",
                "Multi-tenant isolation",
                "Organization management",
                "Branch/location management",
                "Role-based access control",
                "Permission system",
                "Product catalog",
                "Customer management",
                "Supplier management",
                "Inventory stock tracking",
                "Stock movement audit trail",
                "Stock reservations",
                "Repository pattern",
                "Database migrations",
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2 text-xs p-2 rounded bg-gray-950/50">
                  <span className="text-blue-400">✓</span>
                  <span className="text-gray-400">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stage 3 Completion Details */}
      {activeStage === 2 && (
        <div className="mt-8 rounded-xl border border-amber-500/30 bg-amber-500/5 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">✅</span>
            <div>
              <h4 className="text-lg font-bold text-amber-400">Stage 3 — Transactions Complete</h4>
              <p className="text-xs text-gray-400">All transaction entities and financial operations implemented</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Domain Entities</h5>
              <div className="space-y-1.5">
                {[
                  "app/domain/sales/entities.py",
                  "app/domain/purchases/entities.py",
                  "app/domain/payments/entities.py",
                  "app/domain/receivables/entities.py",
                  "app/domain/payables/entities.py",
                  "app/domain/closing/entities.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-amber-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Infrastructure</h5>
              <div className="space-y-1.5">
                {[
                  "app/infrastructure/database/models/sales.py",
                  "app/infrastructure/database/models/purchases.py",
                  "app/infrastructure/database/models/payments.py",
                  "app/infrastructure/database/models/receivables.py",
                  "app/infrastructure/database/models/payables.py",
                  "app/infrastructure/database/models/closing.py",
                  "migrations/versions/003_transactions.py",
                ].map((file) => (
                  <div key={file} className="flex items-center gap-2 text-xs">
                    <span className="text-amber-400">✓</span>
                    <code className="text-gray-400">{file}</code>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-4">
            <h5 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">Key Features Implemented</h5>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {[
                "Sales order management",
                "Purchase order management",
                "Payment processing",
                "Receivables tracking",
                "Payables tracking",
                "Daily closing operations",
                "Transaction audit trails",
                "Multi-currency support",
                "Payment allocations",
                "Status workflows",
                "Fixed-precision decimals",
                "Tenant isolation",
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2 text-xs p-2 rounded bg-gray-950/50">
                  <span className="text-amber-400">✓</span>
                  <span className="text-gray-400">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
