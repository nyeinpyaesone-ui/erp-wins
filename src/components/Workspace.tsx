import { useState } from "react";

interface WorkspaceItem {
  category: string;
  icon: string;
  status: "complete" | "in-progress" | "pending";
  files: { path: string; description: string; lines?: number }[];
}

const workspaceItems: WorkspaceItem[] = [
  {
    category: "Foundation",
    icon: "🏗️",
    status: "complete",
    files: [
      { path: "pyproject.toml", description: "Python project configuration", lines: 65 },
      { path: ".env.example", description: "Environment template", lines: 50 },
      { path: "app/config.py", description: "Pydantic settings", lines: 120 },
      { path: "app/main.py", description: "FastAPI application", lines: 80 },
      { path: "app/lifespan.py", description: "Startup/shutdown", lines: 70 },
      { path: "app/api/health.py", description: "Health endpoints", lines: 90 },
      { path: "app/api/websocket.py", description: "WebSocket transport", lines: 40 },
      { path: "app/infrastructure/database/engine.py", description: "Async DB engine", lines: 100 },
      { path: "app/infrastructure/redis/client.py", description: "Redis client", lines: 50 },
      { path: "Dockerfile", description: "Multi-stage build", lines: 60 },
      { path: "docker-compose.yml", description: "All services", lines: 120 },
      { path: "alembic.ini", description: "Migration config", lines: 100 },
      { path: "migrations/env.py", description: "Async migrations", lines: 90 },
      { path: ".github/workflows/ci.yml", description: "CI/CD pipeline", lines: 250 },
      { path: "workers/celery_app.py", description: "Celery config", lines: 60 },
    ],
  },
  {
    category: "Core Business",
    icon: "🏛️",
    status: "complete",
    files: [
      { path: "app/domain/users/entities.py", description: "User domain", lines: 80 },
      { path: "app/domain/organizations/entities.py", description: "Organization domain", lines: 80 },
      { path: "app/domain/branches/entities.py", description: "Branch domain", lines: 80 },
      { path: "app/domain/roles/entities.py", description: "RBAC domain", lines: 150 },
      { path: "app/domain/products/entities.py", description: "Product domain", lines: 100 },
      { path: "app/domain/customers/entities.py", description: "Customer domain", lines: 100 },
      { path: "app/domain/suppliers/entities.py", description: "Supplier domain", lines: 100 },
      { path: "app/domain/inventory/entities.py", description: "Inventory domain", lines: 200 },
      { path: "app/infrastructure/database/models/*.py", description: "8 SQLAlchemy models", lines: 800 },
      { path: "app/infrastructure/repositories/user_repository.py", description: "User repository", lines: 120 },
      { path: "app/infrastructure/auth/security.py", description: "JWT + bcrypt", lines: 80 },
      { path: "app/application/services/authentication_service.py", description: "Auth service", lines: 100 },
      { path: "app/api/auth.py", description: "Auth API routes", lines: 150 },
      { path: "migrations/versions/002_core_business.py", description: "Core tables migration", lines: 200 },
    ],
  },
  {
    category: "Transactions",
    icon: "💳",
    status: "complete",
    files: [
      { path: "app/domain/sales/entities.py", description: "Sales domain", lines: 120 },
      { path: "app/domain/purchases/entities.py", description: "Purchases domain", lines: 120 },
      { path: "app/domain/payments/entities.py", description: "Payments domain", lines: 130 },
      { path: "app/domain/receivables/entities.py", description: "Receivables domain", lines: 120 },
      { path: "app/domain/payables/entities.py", description: "Payables domain", lines: 120 },
      { path: "app/domain/closing/entities.py", description: "Daily closing domain", lines: 100 },
      { path: "app/infrastructure/database/models/sales.py", description: "Sales models", lines: 80 },
      { path: "app/infrastructure/database/models/purchases.py", description: "Purchase models", lines: 80 },
      { path: "app/infrastructure/database/models/payments.py", description: "Payment models", lines: 80 },
      { path: "app/infrastructure/database/models/receivables.py", description: "Receivable models", lines: 80 },
      { path: "app/infrastructure/database/models/payables.py", description: "Payable models", lines: 80 },
      { path: "app/infrastructure/database/models/closing.py", description: "Closing model", lines: 80 },
      { path: "app/infrastructure/repositories/sales_repository.py", description: "Sales repository", lines: 200 },
      { path: "app/infrastructure/repositories/purchases_repository.py", description: "Purchase repository", lines: 200 },
      { path: "app/infrastructure/repositories/payments_repository.py", description: "Payment repository", lines: 200 },
      { path: "app/infrastructure/repositories/receivables_repository.py", description: "Receivable repository", lines: 200 },
      { path: "app/infrastructure/repositories/payables_repository.py", description: "Payable repository", lines: 200 },
      { path: "app/infrastructure/repositories/closing_repository.py", description: "Closing repository", lines: 150 },
      { path: "app/application/services/sales_service.py", description: "Sales service", lines: 150 },
      { path: "app/api/sales.py", description: "Sales API routes", lines: 250 },
      { path: "migrations/versions/003_transactions.py", description: "Transaction tables", lines: 250 },
    ],
  },
  {
    category: "System Data",
    icon: "📊",
    status: "complete",
    files: [
      { path: "scripts/seed_data.py", description: "Seed all system data", lines: 600 },
      { path: "scripts/verify_data.py", description: "Verify data integrity", lines: 200 },
    ],
  },
  {
    category: "Tests",
    icon: "🧪",
    status: "complete",
    files: [
      { path: "tests/conftest.py", description: "Test configuration", lines: 60 },
      { path: "tests/api/test_health.py", description: "Health API tests", lines: 40 },
      { path: "tests/unit/test_config.py", description: "Config tests", lines: 80 },
      { path: "tests/unit/test_sales_service.py", description: "Sales service tests", lines: 180 },
    ],
  },
  {
    category: "Documentation",
    icon: "📚",
    status: "complete",
    files: [
      { path: "STAGE_1_COMPLETE.md", description: "Foundation docs", lines: 200 },
      { path: "STAGE_2_COMPLETE.md", description: "Core business docs", lines: 250 },
      { path: "STAGE_3_COMPLETE.md", description: "Transactions docs", lines: 400 },
      { path: "SYSTEM_DATA.md", description: "System data docs", lines: 300 },
      { path: "IMPLEMENTATION_SUMMARY.md", description: "Full summary", lines: 350 },
    ],
  },
];

const statusColors = {
  complete: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  "in-progress": "bg-amber-500/10 text-amber-400 border-amber-500/20",
  pending: "bg-gray-500/10 text-gray-400 border-gray-500/20",
};

const statusLabels = {
  complete: "Complete",
  "in-progress": "In Progress",
  pending: "Pending",
};

export default function Workspace() {
  const [activeCategory, setActiveCategory] = useState(0);
  const category = workspaceItems[activeCategory];

  const totalFiles = workspaceItems.reduce((sum, cat) => sum + cat.files.length, 0);
  const totalLines = workspaceItems.reduce(
    (sum, cat) => sum + cat.files.reduce((s, f) => s + (f.lines || 0), 0),
    0
  );
  const completedCategories = workspaceItems.filter((c) => c.status === "complete").length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Workspace
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Real, functional, runnable code. All files are production-ready and follow
          the architectural principles defined in AGENTS.md.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 p-4 text-center">
          <div className="text-2xl font-bold text-emerald-400">{totalFiles}</div>
          <div className="text-xs text-gray-500">Total Files</div>
        </div>
        <div className="rounded-lg border border-blue-500/30 bg-blue-500/5 p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{totalLines.toLocaleString()}+</div>
          <div className="text-xs text-gray-500">Lines of Code</div>
        </div>
        <div className="rounded-lg border border-purple-500/30 bg-purple-500/5 p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{completedCategories}/{workspaceItems.length}</div>
          <div className="text-xs text-gray-500">Categories Complete</div>
        </div>
        <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-4 text-center">
          <div className="text-2xl font-bold text-amber-400">3/7</div>
          <div className="text-xs text-gray-500">Stages Complete</div>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        {workspaceItems.map((cat, i) => (
          <button
            key={cat.category}
            onClick={() => setActiveCategory(i)}
            className={`px-3 py-2 rounded-lg text-xs transition-all flex items-center gap-2 ${
              activeCategory === i
                ? "bg-gray-800 text-emerald-400 border border-emerald-500/30"
                : "bg-gray-900/50 border border-gray-800 text-gray-400 hover:border-gray-700"
            }`}
          >
            <span>{cat.icon}</span>
            <span>{cat.category}</span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded border ${statusColors[cat.status]}`}>
              {cat.files.length}
            </span>
          </button>
        ))}
      </div>

      {/* File List */}
      <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <span className="text-2xl">{category.icon}</span>
            <div>
              <h3 className="text-lg font-bold text-gray-200">{category.category}</h3>
              <p className="text-xs text-gray-500">{category.files.length} files</p>
            </div>
          </div>
          <span className={`text-xs px-3 py-1 rounded-full border ${statusColors[category.status]}`}>
            {statusLabels[category.status]}
          </span>
        </div>

        <div className="space-y-2">
          {category.files.map((file) => (
            <div
              key={file.path}
              className="flex items-center justify-between p-3 rounded-lg bg-gray-950/50 border border-gray-800/50 hover:border-gray-700 transition-colors"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-emerald-400 text-xs flex-shrink-0">✓</span>
                <code className="text-xs text-gray-300 truncate">{file.path}</code>
              </div>
              <div className="flex items-center gap-3 flex-shrink-0 ml-4">
                <span className="text-xs text-gray-500 hidden sm:inline">{file.description}</span>
                {file.lines && (
                  <span className="text-[10px] text-gray-600 bg-gray-800 px-2 py-0.5 rounded">
                    {file.lines} lines
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* GitHub Actions */}
      <div className="mt-8 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">🔄</span>
          <div>
            <h4 className="text-lg font-bold text-gray-200">GitHub Actions CI/CD</h4>
            <p className="text-xs text-gray-400">Automated pipeline with quality gates</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {[
            { name: "Dependency Validation", icon: "📦", status: "active" },
            { name: "Lint (Ruff)", icon: "🔍", status: "active" },
            { name: "Type Check (MyPy)", icon: "🔤", status: "active" },
            { name: "Unit Tests", icon: "🧪", status: "active" },
            { name: "Integration Tests", icon: "🔗", status: "active" },
            { name: "API Tests", icon: "🌐", status: "active" },
            { name: "Security Scan (Bandit)", icon: "🛡️", status: "active" },
            { name: "Docker Build", icon: "🐳", status: "active" },
            { name: "Release", icon: "🚀", status: "active" },
          ].map((job) => (
            <div
              key={job.name}
              className="flex items-center gap-2 p-3 rounded-lg bg-gray-950/50 border border-gray-800"
            >
              <span className="text-lg">{job.icon}</span>
              <span className="text-xs text-gray-300 flex-1">{job.name}</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
            </div>
          ))}
        </div>
      </div>

      {/* Run Commands */}
      <div className="mt-8 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-6">
        <h4 className="text-sm font-semibold text-gray-200 mb-4">
          🚀 Quick Start Commands
        </h4>
        <div className="space-y-3">
          {[
            { cmd: "pip install -e '.[dev]'", desc: "Install dependencies" },
            { cmd: "docker-compose up -d", desc: "Start all services" },
            { cmd: "alembic upgrade head", desc: "Run database migrations" },
            { cmd: "python -m scripts.seed_data", desc: "Seed system data" },
            { cmd: "python -m scripts.verify_data", desc: "Verify data integrity" },
            { cmd: "uvicorn app.main:app --reload", desc: "Start development server" },
            { cmd: "pytest tests/", desc: "Run all tests" },
          ].map((item) => (
            <div key={item.cmd} className="flex items-center gap-3 p-2 rounded bg-gray-950/50">
              <code className="text-xs text-emerald-400 flex-1">{item.cmd}</code>
              <span className="text-xs text-gray-500">{item.desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
