import { useState } from "react";

interface Domain {
  name: string;
  icon: string;
  color: string;
  owns: string[];
  rules: string[];
}

const domains: Domain[] = [
  {
    name: "Finance",
    icon: "💰",
    color: "emerald",
    owns: ["Transactions", "Ledgers", "Accounts", "Currencies"],
    rules: [
      "Financial operations must be transactional and auditable",
      "Never use floating-point for monetary amounts",
      "Financial totals are server/database authoritative",
      "Currency must be explicit",
    ],
  },
  {
    name: "Inventory",
    icon: "📦",
    color: "blue",
    owns: ["Products", "SKUs", "Warehouses", "Stock", "Reservations", "Movements"],
    rules: [
      "Stock-changing operations are transactional",
      "Prevent overselling through transactional consistency",
      "Maintain auditable stock-movement history",
      "Inventory balances must be reproducible from authoritative records",
    ],
  },
  {
    name: "Sales",
    icon: "🛒",
    color: "amber",
    owns: ["Orders", "Invoices", "Quotations", "Returns"],
    rules: [
      "Orders and payments must be idempotent",
      "Financial totals are server authoritative",
      "Never trust client-provided financial totals",
    ],
  },
  {
    name: "E-Commerce",
    icon: "🌐",
    color: "purple",
    owns: ["Sellers", "Products", "Carts", "Orders", "Reviews", "Messaging"],
    rules: [
      "Uses shared inventory and finance through defined interfaces",
      "Do not duplicate authoritative financial or inventory state",
      "External marketplace events must be verified before processing",
    ],
  },
  {
    name: "Logistics",
    icon: "🚚",
    color: "cyan",
    owns: ["Shipments", "Tracking", "Carriers", "Routes"],
    rules: [
      "External calls require timeout, retry, error classification",
      "Provider-specific SDK logic must not spread through domain code",
    ],
  },
  {
    name: "HR",
    icon: "👥",
    color: "pink",
    owns: ["Employees", "Payroll", "Attendance", "Roles"],
    rules: [
      "Authorization is always server-side",
      "Important business changes are auditable",
    ],
  },
  {
    name: "SME",
    icon: "🏢",
    color: "orange",
    owns: ["Branches", "Customers", "Suppliers", "Daily Closing", "Debts"],
    rules: [
      "Support Myanmar language and MMK",
      "Daily closing must be transactional",
      "Customer debts and supplier payables are authoritative",
    ],
  },
];

const colorMap: Record<string, { border: string; bg: string; text: string; badge: string }> = {
  emerald: { border: "border-emerald-500/30", bg: "bg-emerald-500/5", text: "text-emerald-400", badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
  blue: { border: "border-blue-500/30", bg: "bg-blue-500/5", text: "text-blue-400", badge: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
  amber: { border: "border-amber-500/30", bg: "bg-amber-500/5", text: "text-amber-400", badge: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
  purple: { border: "border-purple-500/30", bg: "bg-purple-500/5", text: "text-purple-400", badge: "bg-purple-500/10 text-purple-400 border-purple-500/20" },
  cyan: { border: "border-cyan-500/30", bg: "bg-cyan-500/5", text: "text-cyan-400", badge: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20" },
  pink: { border: "border-pink-500/30", bg: "bg-pink-500/5", text: "text-pink-400", badge: "bg-pink-500/10 text-pink-400 border-pink-500/20" },
  orange: { border: "border-orange-500/30", bg: "bg-orange-500/5", text: "text-orange-400", badge: "bg-orange-500/10 text-orange-400 border-orange-500/20" },
};

export default function DomainBoundaries() {
  const [activeDomain, setActiveDomain] = useState(0);
  const domain = domains[activeDomain];
  const colors = colorMap[domain.color];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Domain Boundaries
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Each domain owns its entities, value objects, services, policies, repository interfaces,
          events, and exceptions. Domains must not directly modify another domain's tables.
        </p>
      </div>

      {/* Domain Selector */}
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        {domains.map((d, i) => (
          <button
            key={d.name}
            onClick={() => setActiveDomain(i)}
            className={`px-3 py-2 rounded-lg text-xs transition-all flex items-center gap-2 ${
              activeDomain === i
                ? `${colorMap[d.color].bg} ${colorMap[d.color].border} border ${colorMap[d.color].text}`
                : "bg-gray-900/50 border border-gray-800 text-gray-400 hover:border-gray-700"
            }`}
          >
            <span>{d.icon}</span>
            <span>{d.name}</span>
          </button>
        ))}
      </div>

      {/* Domain Detail */}
      <div className={`rounded-xl border ${colors.border} ${colors.bg} p-6 sm:p-8`}>
        <div className="flex items-center gap-4 mb-6">
          <span className="text-3xl">{domain.icon}</span>
          <div>
            <h3 className={`text-xl font-bold ${colors.text}`}>{domain.name}</h3>
            <p className="text-xs text-gray-500">domain/{domain.name.toLowerCase()}/</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">
              Owns
            </h4>
            <div className="flex flex-wrap gap-2">
              {domain.owns.map((item) => (
                <span
                  key={item}
                  className={`text-xs px-3 py-1.5 rounded-lg border ${colors.badge}`}
                >
                  {item}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-3">
              Rules
            </h4>
            <ul className="space-y-2">
              {domain.rules.map((rule, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className={`${colors.text} text-xs mt-0.5`}>›</span>
                  <span className="text-xs text-gray-400">{rule}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Cross-Domain Rules */}
      <div className="mt-8 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <h4 className="text-sm font-semibold text-gray-200 mb-4">
          🔒 Cross-Domain Communication Rules
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="p-3 rounded-lg bg-gray-950 border border-gray-800">
            <div className="text-xs text-emerald-400 mb-1">Synchronous</div>
            <p className="text-xs text-gray-400">
              Cross-domain synchronous operations use application contracts (interfaces).
            </p>
          </div>
          <div className="p-3 rounded-lg bg-gray-950 border border-gray-800">
            <div className="text-xs text-amber-400 mb-1">Asynchronous</div>
            <p className="text-xs text-gray-400">
              Cross-domain asynchronous consequences use domain events via transactional outbox.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
