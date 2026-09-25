import { useState } from "react";

interface Step {
  id: number;
  name: string;
  description: string;
  icon: string;
  category: "validation" | "installation" | "build" | "finalization";
  details: string[];
}

const steps: Step[] = [
  {
    id: 1,
    name: "Validate Windows 10",
    description: "Checks that the OS is Windows 10 via registry",
    icon: "🪟",
    category: "validation",
    details: [
      "Reads HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
      "Verifies ProductName contains 'Windows 10'",
      "Logs the detected build number",
    ],
  },
  {
    id: 2,
    name: "Validate Architecture",
    description: "Ensures x64 (AMD64) processor architecture",
    icon: "⚙️",
    category: "validation",
    details: [
      "Checks PROCESSOR_ARCHITECTURE environment variable",
      "Requires AMD64 architecture",
      "Blocks ARM and x86 systems",
    ],
  },
  {
    id: 3,
    name: "Validate Admin Access",
    description: "Requires elevated administrator privileges",
    icon: "🔐",
    category: "validation",
    details: [
      "Uses WindowsPrincipal for role check",
      "Checks WindowsBuiltInRole::Administrator",
      "Fails if not running as admin",
    ],
  },
  {
    id: 4,
    name: "Validate PowerShell",
    description: "Ensures PowerShell 5.1 or newer",
    icon: "💻",
    category: "validation",
    details: [
      "Checks $PSVersionTable.PSVersion.Major",
      "Requires version 5 or higher",
      "Compatible with Windows 10 default",
    ],
  },
  {
    id: 5,
    name: "Validate Repository",
    description: "Confirms the directory contains a valid project",
    icon: "📁",
    category: "validation",
    details: [
      "Walks up directory tree to find .git",
      "Checks for package.json, pyproject.toml, or requirements.txt",
      "Sets repository root for all subsequent operations",
    ],
  },
  {
    id: 6,
    name: "Validate Runtime Tooling",
    description: "Checks for git, node, npm, and python availability",
    icon: "🔧",
    category: "validation",
    details: [
      "Requires git.exe for repository operations",
      "Checks node.exe and npm.cmd if Node projects found",
      "Validates py.exe if Python requirements detected",
    ],
  },
  {
    id: 7,
    name: "Prepare Data Directories",
    description: "Creates application data directories in ProgramData",
    icon: "📂",
    category: "installation",
    details: [
      "Creates %ProgramData%\\ERP\\logs",
      "Creates %ProgramData%\\ERP\\data",
      "Creates %ProgramData%\\ERP\\backups",
      "Creates %ProgramData%\\ERP\\config",
    ],
  },
  {
    id: 8,
    name: "Install Node Dependencies",
    description: "Runs npm ci / pnpm install / yarn install for all projects",
    icon: "📦",
    category: "installation",
    details: [
      "Detects all package.json files recursively",
      "Uses lockfile-appropriate installer (npm ci, pnpm, yarn)",
      "Skips node_modules, dist, and build directories",
    ],
  },
  {
    id: 9,
    name: "Initialize Python Environments",
    description: "Creates venvs and installs Python dependencies",
    icon: "🐍",
    category: "installation",
    details: [
      "Creates .venv using py.exe -3.12",
      "Bootstraps pip, setuptools, wheel",
      "Installs from requirements*.txt files",
    ],
  },
  {
    id: 10,
    name: "Run Database Migrations",
    description: "Executes Alembic migrations for all detected configs",
    icon: "🗄️",
    category: "build",
    details: [
      "Finds all alembic.ini files recursively",
      "Uses venv Python or system alembic.exe",
      "Runs 'alembic upgrade head'",
      "Skippable with -SkipMigrations flag",
    ],
  },
  {
    id: 11,
    name: "Build Node Applications",
    description: "Runs npm run build for all Node projects",
    icon: "🏗️",
    category: "build",
    details: [
      "Checks for 'build' script in package.json",
      "Executes npm run build in each project",
      "Skippable with -SkipBuild flag",
    ],
  },
  {
    id: 12,
    name: "Validate & Finalize",
    description: "Validates build artifacts and writes setup state",
    icon: "✅",
    category: "finalization",
    details: [
      "Checks dist/build directories are non-empty",
      "Writes setup-state.json to ProgramData",
      "Records completion timestamp and repo path",
    ],
  },
];

const categoryColors: Record<string, string> = {
  validation: "border-blue-500/30 bg-blue-500/5",
  installation: "border-emerald-500/30 bg-emerald-500/5",
  build: "border-amber-500/30 bg-amber-500/5",
  finalization: "border-purple-500/30 bg-purple-500/5",
};

const categoryLabels: Record<string, string> = {
  validation: "Validation",
  installation: "Installation",
  build: "Build",
  finalization: "Finalization",
};

const categoryBadgeColors: Record<string, string> = {
  validation: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  installation: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  build: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  finalization: "bg-purple-500/10 text-purple-400 border-purple-500/20",
};

export default function SetupSteps() {
  const [expandedStep, setExpandedStep] = useState<number | null>(null);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Setup Pipeline
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto">
          The script executes these steps in order, each wrapped in error handling
          with detailed logging.
        </p>
      </div>

      {/* Category Legend */}
      <div className="flex flex-wrap justify-center gap-3 mb-10">
        {Object.entries(categoryLabels).map(([key, label]) => (
          <span
            key={key}
            className={`text-xs px-3 py-1 rounded-full border ${categoryBadgeColors[key]}`}
          >
            {label}
          </span>
        ))}
      </div>

      {/* Steps Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {steps.map((step) => (
          <div
            key={step.id}
            className={`rounded-xl border p-5 transition-all cursor-pointer hover:scale-[1.02] ${
              categoryColors[step.category]
            } ${expandedStep === step.id ? "ring-1 ring-emerald-500/30" : ""}`}
            onClick={() =>
              setExpandedStep(expandedStep === step.id ? null : step.id)
            }
          >
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-gray-800 flex items-center justify-center text-sm">
                {step.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs text-gray-500">#{step.id}</span>
                  <span
                    className={`text-[10px] px-1.5 py-0.5 rounded border ${categoryBadgeColors[step.category]}`}
                  >
                    {categoryLabels[step.category]}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-gray-200 mb-1">
                  {step.name}
                </h3>
                <p className="text-xs text-gray-500">{step.description}</p>
              </div>
            </div>

            {expandedStep === step.id && (
              <div className="mt-4 pt-4 border-t border-gray-700/50">
                <ul className="space-y-2">
                  {step.details.map((detail, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-emerald-400 text-xs mt-0.5">›</span>
                      <span className="text-xs text-gray-400">{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
