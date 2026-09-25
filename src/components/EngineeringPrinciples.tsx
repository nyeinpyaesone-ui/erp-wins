import { useState } from "react";

interface Principle {
  title: string;
  icon: string;
  description: string;
  rules: string[];
  category: "transaction" | "security" | "event" | "ai" | "ops";
}

const principles: Principle[] = [
  {
    title: "Transactional Outbox",
    icon: "📬",
    description: "Reliable domain events using the transactional outbox pattern. Events and business state share the same transaction.",
    rules: [
      "Event creation and business-state mutation share the same transaction",
      "Dispatch must tolerate duplicate delivery",
      "Publication must be observable",
      "Failed events must remain recoverable",
      "Outbox processing must use bounded batches",
    ],
    category: "event",
  },
  {
    title: "Idempotency",
    icon: "🔁",
    description: "Retryable operations must use stable idempotency keys. Required for orders, payments, webhooks, event consumers, and agent actions.",
    rules: [
      "Idempotency records prevent duplicate business effects",
      "Do not use timestamps or random values as implicit keys",
      "Caller should provide stable operation identifiers",
    ],
    category: "transaction",
  },
  {
    title: "LLM Security",
    icon: "🛡️",
    description: "LLM output is untrusted. LLMs must never directly execute SQL, shell commands, Python, database mutations, or financial transactions.",
    rules: [
      "LLM → Structured Proposal → Schema Validation → Policy → Authorization → Execute",
      "LLM-generated values must be treated as untrusted input",
      "LLM confidence is never authorization",
    ],
    category: "ai",
  },
  {
    title: "Decision Engine",
    icon: "🧠",
    description: "Use deterministic rules first. LLM is only used when deterministic rules cannot resolve the decision.",
    rules: [
      "Deterministic Rules → Resolved → Execute",
      "Unresolved → LLM → Structured Proposal → Policy Gate → Execute / Escalate / Reject",
      "Prefer deterministic for financial calculations, permissions, compliance",
    ],
    category: "ai",
  },
  {
    title: "Retry Policy",
    icon: "⏱️",
    description: "Retry only transient failures. Never retry validation, authorization, or permanent business-rule failures.",
    rules: [
      "Failure → Classify → Transient → Backoff → Retry → Max Attempts → Dead Letter",
      "Use bounded exponential backoff with jitter",
      "Never use infinite retries",
    ],
    category: "ops",
  },
  {
    title: "Authorization",
    icon: "🔐",
    description: "Authorization is always server-side. Separate authentication (identity), authorization (permission), and business policy (operation validity).",
    rules: [
      "Check tenant scope before resource access",
      "Deny by default, apply least privilege",
      "Do not infer authorization from LLM output",
      "Never trust client-provided authorization or tenant identity",
    ],
    category: "security",
  },
  {
    title: "Audit Logging",
    icon: "📝",
    description: "Important business state changes must be auditable with actor, tenant, operation, resource, timestamp, and before/after state.",
    rules: [
      "Never log passwords, tokens, API keys, private keys, or payment credentials",
      "Audit records must not depend solely on client-side logging",
      "Record correlation IDs for traceability",
    ],
    category: "security",
  },
  {
    title: "AI Gateway",
    icon: "🌐",
    description: "All LLM access must go through the AI Gateway. The gateway controls model selection, timeout, token budget, retry, and usage tracking.",
    rules: [
      "Business logic must not call providers directly",
      "External AI transmission requires explicit authorization",
      "LLM calls must have bounded timeouts and resource limits",
    ],
    category: "ai",
  },
];

const categoryColors: Record<string, string> = {
  transaction: "border-emerald-500/30 bg-emerald-500/5",
  security: "border-red-500/30 bg-red-500/5",
  event: "border-blue-500/30 bg-blue-500/5",
  ai: "border-purple-500/30 bg-purple-500/5",
  ops: "border-amber-500/30 bg-amber-500/5",
};

const categoryBadge: Record<string, string> = {
  transaction: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  security: "bg-red-500/10 text-red-400 border-red-500/20",
  event: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  ai: "bg-purple-500/10 text-purple-400 border-purple-500/20",
  ops: "bg-amber-500/10 text-amber-400 border-amber-500/20",
};

const categoryLabels: Record<string, string> = {
  transaction: "Transaction",
  security: "Security",
  event: "Events",
  ai: "AI / LLM",
  ops: "Operations",
};

export default function EngineeringPrinciples() {
  const [filter, setFilter] = useState<string>("all");

  const filtered = filter === "all" ? principles : principles.filter((p) => p.category === filter);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Engineering Principles
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Core principles that govern the platform's design and implementation.
          Correctness takes priority over performance. Simplicity over unnecessary complexity.
        </p>
      </div>

      {/* Filter */}
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        <button
          onClick={() => setFilter("all")}
          className={`px-3 py-1.5 rounded-full text-xs border transition-colors ${
            filter === "all"
              ? "bg-gray-800 text-gray-200 border-gray-600"
              : "bg-gray-900/50 text-gray-500 border-gray-800 hover:border-gray-700"
          }`}
        >
          All
        </button>
        {Object.entries(categoryLabels).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-3 py-1.5 rounded-full text-xs border transition-colors ${
              filter === key
                ? categoryBadge[key]
                : "bg-gray-900/50 text-gray-500 border-gray-800 hover:border-gray-700"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Principles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((principle) => (
          <div
            key={principle.title}
            className={`rounded-xl border p-5 ${categoryColors[principle.category]}`}
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xl">{principle.icon}</span>
              <div>
                <h3 className="text-sm font-semibold text-gray-200">{principle.title}</h3>
                <span className={`text-[10px] px-1.5 py-0.5 rounded border ${categoryBadge[principle.category]}`}>
                  {categoryLabels[principle.category]}
                </span>
              </div>
            </div>
            <p className="text-xs text-gray-400 mb-4 leading-relaxed">{principle.description}</p>
            <ul className="space-y-1.5">
              {principle.rules.map((rule, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-emerald-400 text-xs mt-0.5 flex-shrink-0">›</span>
                  <span className="text-xs text-gray-400">{rule}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Non-Negotiable Rules */}
      <div className="mt-12 rounded-xl border border-red-500/20 bg-red-500/5 p-6">
        <h3 className="text-lg font-semibold text-gray-200 mb-2 flex items-center gap-2">
          <span className="text-red-400">⚠️</span>
          Top 10 Non-Negotiable Rules
        </h3>
        <p className="text-xs text-gray-500 mb-4">These rules cannot be violated under any circumstances.</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {[
            "PostgreSQL owns authoritative business state",
            "Business invariants are transactional",
            "Domain events use transactional outbox",
            "Redis is not authoritative business storage",
            "Domain code does not depend on infrastructure",
            "LLM output is untrusted",
            "LLMs cannot directly mutate business state",
            "High-risk actions require human approval",
            "Cross-domain direct DB manipulation is prohibited",
            "Secrets must never be committed or logged",
          ].map((rule, i) => (
            <div key={i} className="flex items-start gap-2 p-2 rounded bg-gray-950/50">
              <span className="text-red-400 text-xs font-bold">{i + 1}.</span>
              <span className="text-xs text-gray-400">{rule}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
