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
                ERP v1.2.0 LTS
              </span>
            </div>
            <p className="text-xs text-gray-500 leading-relaxed">
              Production-oriented, idempotent setup script for enterprise
              resource planning deployment. Designed for Windows 10 x64
              environments.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">
              Script Info
            </h4>
            <ul className="space-y-2">
              {[
                { label: "Version", value: "1.2.0 LTS" },
                { label: "Platform", value: "Windows 10 x64" },
                { label: "Language", value: "PowerShell 5.1+" },
                { label: "License", value: "Proprietary" },
              ].map((item) => (
                <li key={item.label} className="flex items-center justify-between text-xs">
                  <span className="text-gray-500">{item.label}</span>
                  <span className="text-gray-300">{item.value}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* File Locations */}
          <div>
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">
              File Locations
            </h4>
            <ul className="space-y-2">
              {[
                { label: "Log File", path: "%ProgramData%\\ERP\\logs\\setup.log" },
                { label: "State File", path: "%ProgramData%\\ERP\\setup-state.json" },
                { label: "Data Dir", path: "%ProgramData%\\ERP\\data" },
                { label: "Config Dir", path: "%ProgramData%\\ERP\\config" },
              ].map((item) => (
                <li key={item.label} className="text-xs">
                  <span className="text-gray-500">{item.label}: </span>
                  <code className="text-emerald-400/80">{item.path}</code>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-600">
            ERP v1.2.0 LTS Setup Script Documentation
          </p>
          <div className="flex items-center gap-4">
            <span className="text-xs text-gray-600">
              Run with: <code className="text-gray-400">powershell -ExecutionPolicy Bypass -File .\setup.ps1</code>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
