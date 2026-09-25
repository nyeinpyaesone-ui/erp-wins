export default function Hero() {
  return (
    <div id="overview" className="relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-950 via-gray-900 to-emerald-950/30" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-emerald-900/20 via-transparent to-transparent" />
      
      {/* Grid pattern */}
      <div className="absolute inset-0 opacity-[0.03]" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
      }} />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/80 border border-gray-700 mb-8">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-gray-300">Production Ready • Windows 10 x64</span>
          </div>

          {/* Title */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6">
            <span className="text-gray-100">ERP </span>
            <span className="text-emerald-400">v1.2.0</span>
            <span className="text-gray-100"> LTS</span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-8">
            Production-oriented, idempotent setup script for enterprise resource planning deployment on Windows 10 x64.
          </p>

          {/* Command */}
          <div className="inline-flex items-center gap-3 px-5 py-3 rounded-xl bg-gray-900 border border-gray-700 shadow-2xl shadow-emerald-500/5">
            <span className="text-emerald-400 text-sm">PS&gt;</span>
            <code className="text-sm text-gray-300">
              powershell -ExecutionPolicy Bypass -File .\setup.ps1
            </code>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-12 max-w-3xl mx-auto">
            {[
              { label: "Setup Steps", value: "12" },
              { label: "Functions", value: "18" },
              { label: "Platforms", value: "Win10 x64" },
              { label: "Idempotent", value: "Yes" },
            ].map((stat) => (
              <div
                key={stat.label}
                className="px-4 py-3 rounded-lg bg-gray-800/50 border border-gray-700/50"
              >
                <div className="text-lg font-bold text-emerald-400">{stat.value}</div>
                <div className="text-xs text-gray-500">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-gray-950 to-transparent" />
    </div>
  );
}
