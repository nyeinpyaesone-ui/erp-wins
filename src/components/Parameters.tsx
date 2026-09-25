import { useState } from "react";

interface Parameter {
  name: string;
  type: string;
  default: string;
  description: string;
  example: string;
}

const parameters: Parameter[] = [
  {
    name: "-SkipBuild",
    type: "switch",
    default: "false",
    description: "Skips the 'npm run build' step for all detected Node.js projects. Useful when artifacts already exist or you only need dependency installation.",
    example: "powershell -ExecutionPolicy Bypass -File .\\setup.ps1 -SkipBuild",
  },
  {
    name: "-SkipMigrations",
    type: "switch",
    default: "false",
    description: "Skips Alembic database migration execution. Use when the database is already up-to-date or you want to handle migrations separately.",
    example: "powershell -ExecutionPolicy Bypass -File .\\setup.ps1 -SkipMigrations",
  },
  {
    name: "-SkipOptional",
    type: "switch",
    default: "false",
    description: "Reserved for future use. Intended to skip optional setup steps that may be added in future versions.",
    example: "powershell -ExecutionPolicy Bypass -File .\\setup.ps1 -SkipOptional",
  },
];

export default function Parameters() {
  const [activeParam, setActiveParam] = useState(0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Script Parameters
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto">
          All parameters are optional switches. The script is fully idempotent — safe to re-run.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Parameter List */}
        <div className="space-y-3">
          {parameters.map((param, index) => (
            <button
              key={param.name}
              onClick={() => setActiveParam(index)}
              className={`w-full text-left p-4 rounded-xl border transition-all ${
                activeParam === index
                  ? "border-emerald-500/30 bg-emerald-500/5 shadow-lg shadow-emerald-500/5"
                  : "border-gray-800 bg-gray-900/50 hover:border-gray-700"
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${activeParam === index ? "bg-emerald-400" : "bg-gray-600"}`} />
                <code className="text-sm font-semibold text-gray-200">{param.name}</code>
              </div>
              <p className="text-xs text-gray-500 mt-1 ml-5">{param.type} • default: {param.default}</p>
            </button>
          ))}
        </div>

        {/* Parameter Detail */}
        <div className="lg:col-span-2 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <code className="text-lg font-bold text-emerald-400">
                {parameters[activeParam].name}
              </code>
              <span className="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-400 border border-gray-700">
                {parameters[activeParam].type}
              </span>
            </div>
            <p className="text-sm text-gray-300 leading-relaxed">
              {parameters[activeParam].description}
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">
                Default Value
              </label>
              <code className="text-sm text-amber-400 bg-gray-800/50 px-3 py-1.5 rounded">
                ${parameters[activeParam].default}
              </code>
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">
                Usage Example
              </label>
              <div className="bg-gray-950 border border-gray-800 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-emerald-400 text-xs">PS&gt;</span>
                  <span className="text-xs text-gray-600">PowerShell</span>
                </div>
                <code className="text-sm text-gray-300 break-all">
                  {parameters[activeParam].example}
                </code>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
