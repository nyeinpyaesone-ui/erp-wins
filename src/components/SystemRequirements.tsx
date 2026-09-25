interface Requirement {
  name: string;
  version: string;
  required: boolean | string;
  purpose: string;
  icon: string;
}

const requirements: Requirement[] = [
  {
    name: "Windows 10",
    version: "Any build",
    required: true,
    purpose: "Target operating system — validated via registry",
    icon: "🪟",
  },
  {
    name: "x64 Architecture",
    version: "AMD64",
    required: true,
    purpose: "Required processor architecture",
    icon: "⚡",
  },
  {
    name: "PowerShell",
    version: "5.1+",
    required: true,
    purpose: "Script execution environment",
    icon: "💻",
  },
  {
    name: "Administrator Privileges",
    version: "—",
    required: true,
    purpose: "Required for system-level operations",
    icon: "🔐",
  },
  {
    name: "Git for Windows",
    version: "Latest",
    required: true,
    purpose: "Repository detection and version control",
    icon: "🔀",
  },
  {
    name: "Node.js LTS",
    version: "18+ / 20+",
    required: "conditional",
    purpose: "Required if Node.js projects are detected",
    icon: "🟢",
  },
  {
    name: "npm",
    version: "9+",
    required: "conditional",
    purpose: "Node.js package management (ships with Node)",
    icon: "📦",
  },
  {
    name: "Python 3.12",
    version: "3.12.x",
    required: "conditional",
    purpose: "Required if Python requirements files are found",
    icon: "🐍",
  },
];

export default function SystemRequirements() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          System Requirements
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto">
          The script validates these requirements before proceeding. Conditional
          requirements are only needed if relevant project files are detected.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {requirements.map((req) => (
          <div
            key={req.name}
            className="group rounded-xl border border-gray-800 bg-gray-900/50 p-5 hover:border-gray-700 transition-all hover:shadow-lg hover:shadow-gray-900/50"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-2xl">{req.icon}</span>
              <span
                className={`text-[10px] px-2 py-0.5 rounded-full border ${
                  req.required === true
                    ? "bg-red-500/10 text-red-400 border-red-500/20"
                    : req.required === "conditional"
                    ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                    : "bg-gray-800 text-gray-400 border-gray-700"
                }`}
              >
                {req.required === true ? "Required" : req.required === "conditional" ? "Conditional" : "Optional"}
              </span>
            </div>
            <h3 className="text-sm font-semibold text-gray-200 mb-1">
              {req.name}
            </h3>
            <p className="text-xs text-emerald-400 mb-2">v{req.version}</p>
            <p className="text-xs text-gray-500">{req.purpose}</p>
          </div>
        ))}
      </div>

      {/* Output Directories */}
      <div className="mt-12 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <h3 className="text-lg font-semibold text-gray-200 mb-4">
          📂 Created Directories
        </h3>
        <p className="text-sm text-gray-400 mb-4">
          The script creates the following directories under <code className="text-emerald-400">%ProgramData%\ERP</code>:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {[
            { path: "ERP\\logs", desc: "Setup and runtime logs" },
            { path: "ERP\\data", desc: "Application data storage" },
            { path: "ERP\\backups", desc: "Database and config backups" },
            { path: "ERP\\config", desc: "Runtime configuration files" },
          ].map((dir) => (
            <div
              key={dir.path}
              className="p-3 rounded-lg bg-gray-950 border border-gray-800"
            >
              <code className="text-xs text-emerald-400 block mb-1">
                %ProgramData%\{dir.path}
              </code>
              <span className="text-xs text-gray-500">{dir.desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
