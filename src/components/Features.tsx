interface Feature {
  title: string;
  description: string;
  icon: string;
  highlights: string[];
}

const features: Feature[] = [
  {
    title: "Idempotent Execution",
    description: "Safe to run multiple times without side effects. The script checks state before every action.",
    icon: "🔄",
    highlights: ["State file tracking", "Conditional directory creation", "Lockfile-aware installs"],
  },
  {
    title: "Structured Logging",
    description: "Every action is logged with timestamps and severity levels to both console and file.",
    icon: "📝",
    highlights: ["INFO / WARN / ERROR levels", "UTF-8 encoded log files", "Stored in %ProgramData%\\ERP\\logs"],
  },
  {
    title: "Multi-Stack Detection",
    description: "Automatically discovers Node.js and Python projects anywhere in the repository tree.",
    icon: "🔍",
    highlights: ["Recursive package.json search", "Requirements.txt detection", "Alembic config discovery"],
  },
  {
    title: "Smart Package Installation",
    description: "Detects lockfile type and uses the appropriate package manager for each project.",
    icon: "📦",
    highlights: ["npm ci for package-lock.json", "pnpm for pnpm-lock.yaml", "yarn for yarn.lock"],
  },
  {
    title: "Python Virtual Environments",
    description: "Creates isolated .venv directories with Python 3.12 and bootstraps pip tooling.",
    icon: "🐍",
    highlights: ["py.exe -3.12 launcher", "Automatic pip upgrade", "Per-project isolation"],
  },
  {
    title: "Build Artifact Validation",
    description: "Verifies that build output directories exist and contain files after compilation.",
    icon: "✅",
    highlights: ["Checks dist/build directories", "Validates non-empty output", "Multiple path candidates"],
  },
  {
    title: "Error Handling",
    description: "Strict mode with Stop on error. Every step is wrapped in try/catch with detailed messages.",
    icon: "🛡️",
    highlights: ["Set-StrictMode -Latest", "Invoke-Step wrapper", "Exit code validation"],
  },
  {
    title: "State Persistence",
    description: "Writes setup state to JSON for tracking completion, timestamps, and repository paths.",
    icon: "💾",
    highlights: ["setup-state.json", "Completion tracking", "ISO 8601 timestamps"],
  },
];

export default function Features() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Key Features
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto">
          Designed for reliability and transparency in production environments.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="group rounded-xl border border-gray-800 bg-gray-900/30 p-5 hover:border-emerald-500/20 hover:bg-gray-900/60 transition-all"
          >
            <div className="text-2xl mb-3">{feature.icon}</div>
            <h3 className="text-sm font-semibold text-gray-200 mb-2">
              {feature.title}
            </h3>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              {feature.description}
            </p>
            <ul className="space-y-1.5">
              {feature.highlights.map((h) => (
                <li key={h} className="flex items-center gap-2">
                  <span className="w-1 h-1 rounded-full bg-emerald-500" />
                  <span className="text-[11px] text-gray-400">{h}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
