import { useState } from "react";

interface DataCategory {
  name: string;
  icon: string;
  count: number;
  color: string;
  items: { label: string; value: string; detail?: string }[];
}

const dataCategories: DataCategory[] = [
  {
    name: "Permissions",
    icon: "🔑",
    count: 47,
    color: "emerald",
    items: [
      { label: "Users", value: "4", detail: "create, read, update, delete" },
      { label: "Organizations", value: "4", detail: "create, read, update, delete" },
      { label: "Branches", value: "4", detail: "create, read, update, delete" },
      { label: "Roles", value: "4", detail: "create, read, update, delete" },
      { label: "Products", value: "4", detail: "create, read, update, delete" },
      { label: "Customers", value: "4", detail: "create, read, update, delete" },
      { label: "Suppliers", value: "4", detail: "create, read, update, delete" },
      { label: "Inventory", value: "4", detail: "create, read, update, delete" },
      { label: "Sales", value: "5", detail: "create, read, update, delete, approve" },
      { label: "Purchases", value: "5", detail: "create, read, update, delete, approve" },
      { label: "Payments", value: "5", detail: "create, read, update, delete, approve" },
      { label: "Reports", value: "2", detail: "read, export" },
      { label: "Daily Closing", value: "3", detail: "create, read, approve" },
    ],
  },
  {
    name: "Roles",
    icon: "👥",
    count: 7,
    color: "blue",
    items: [
      { label: "Super Administrator", value: "SUPER_ADMIN", detail: "Full system access" },
      { label: "Administrator", value: "ADMIN", detail: "Organization-level administration" },
      { label: "Branch Manager", value: "MANAGER", detail: "Branch-level management" },
      { label: "Accountant", value: "ACCOUNTANT", detail: "Financial operations" },
      { label: "Sales Person", value: "SALES_PERSON", detail: "Sales operations" },
      { label: "Inventory Clerk", value: "INVENTORY_CLERK", detail: "Stock management" },
      { label: "Viewer", value: "VIEWER", detail: "Read-only access" },
    ],
  },
  {
    name: "Organization",
    icon: "🏢",
    count: 1,
    color: "purple",
    items: [
      { label: "Name", value: "Demo Trading Company" },
      { label: "Myanmar Name", value: "ဒီမို ကုန်သွယ်ရေး ကုမ္ပဏီ" },
      { label: "Code", value: "DEMO" },
      { label: "Tax ID", value: "TAX-DEMO-001" },
      { label: "Address", value: "No. 123, Pyay Road, Kamayut Township, Yangon" },
      { label: "Phone", value: "+95 9 123 456 789" },
      { label: "Email", value: "info@demotrading.mm" },
    ],
  },
  {
    name: "Branches",
    icon: "🏪",
    count: 4,
    color: "amber",
    items: [
      { label: "HQ", value: "Headquarters", detail: "ဌာနချုပ် — Pyay Road, Yangon" },
      { label: "WH-A", value: "Main Warehouse", detail: "အဓိက ကုန်လှောင်ရုံ — Hlaing Tharyar" },
      { label: "RT-01", value: "Downtown Retail", detail: "မြို့တွင်း လက်လီဆိုင် — Lanmadaw" },
      { label: "RT-02", value: "Mandalay Branch", detail: "မန္တလေး ဆိုင်ခွဲ — 78th Street" },
    ],
  },
  {
    name: "Products",
    icon: "📦",
    count: 12,
    color: "cyan",
    items: [
      { label: "RICE-50K", value: "Ponnyasin Rice (50kg)", detail: "MMK 52,000" },
      { label: "OIL-5L", value: "Golden Star Cooking Oil (5L)", detail: "MMK 14,500" },
      { label: "SUGAR-10K", value: "White Sugar (10kg)", detail: "MMK 18,000" },
      { label: "SALT-1K", value: "Iodized Salt (1kg)", detail: "MMK 1,200" },
      { label: "FISHSAUCE-500", value: "Mega Fish Sauce (500ml)", detail: "MMK 3,200" },
      { label: "NOODLE-P5", value: "Mama Instant Noodles (5 pack)", detail: "MMK 2,000" },
      { label: "ONION-50K", value: "Shan Onion (50kg)", detail: "MMK 32,000" },
      { label: "GARLIC-10K", value: "Shan Garlic (10kg)", detail: "MMK 24,000" },
      { label: "TEA-LB", value: "Shan Tea Leaves (1 viss)", detail: "MMK 11,000" },
      { label: "BEAN-25K", value: "Matpe Bean (25kg)", detail: "MMK 28,000" },
      { label: "DAL-25K", value: "Red Gram Dal (25kg)", detail: "MMK 35,000" },
      { label: "FLOUR-25K", value: "Wheat Flour (25kg)", detail: "MMK 23,000" },
    ],
  },
  {
    name: "Customers",
    icon: "🛒",
    count: 5,
    color: "pink",
    items: [
      { label: "CUST-001", value: "U Aung Min Trading", detail: "Credit: MMK 5,000,000" },
      { label: "CUST-002", value: "Daw Khin Marcy Supermarket", detail: "Credit: MMK 3,000,000" },
      { label: "CUST-003", value: "Ko Zaw Win Retail Shop", detail: "Credit: MMK 1,000,000" },
      { label: "CUST-004", value: "Ma Thida (Walk-in)", detail: "Credit: MMK 200,000" },
      { label: "CUST-005", value: "Myanmar Food Distribution Co.", detail: "Credit: MMK 10,000,000" },
    ],
  },
  {
    name: "Suppliers",
    icon: "🏭",
    count: 5,
    color: "orange",
    items: [
      { label: "SUP-001", value: "Ayeyarwady Rice Mill", detail: "Pathein — Net 30" },
      { label: "SUP-002", value: "Golden Star Oil Factory", detail: "Yangon — Net 15" },
      { label: "SUP-003", value: "Shan Highland Produce", detail: "Taunggyi — COD" },
      { label: "SUP-004", value: "Mega Condiments Myanmar", detail: "Yangon — Net 30" },
      { label: "SUP-005", value: "Mandalay Pulses & Grains", detail: "Mandalay — Net 45" },
    ],
  },
  {
    name: "Inventory",
    icon: "📊",
    count: 48,
    color: "red",
    items: [
      { label: "Stock Records", value: "48", detail: "12 products × 4 branches" },
      { label: "Stock Movements", value: "48", detail: "Initial receipt movements" },
      { label: "Total Cost Value", value: "MMK 892,400,000", detail: "Across all branches" },
      { label: "Total Retail Value", value: "MMK 1,126,800,000", detail: "Across all branches" },
      { label: "HQ Stock", value: "2,470 units", detail: "Retail-ready inventory" },
      { label: "Warehouse Stock", value: "24,500 units", detail: "Bulk storage" },
      { label: "Downtown Retail", value: "740 units", detail: "Retail floor" },
      { label: "Mandalay Branch", value: "950 units", detail: "Regional retail" },
    ],
  },
];

const colorMap: Record<string, { border: string; bg: string; text: string; badge: string }> = {
  emerald: { border: "border-emerald-500/30", bg: "bg-emerald-500/5", text: "text-emerald-400", badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
  blue: { border: "border-blue-500/30", bg: "bg-blue-500/5", text: "text-blue-400", badge: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
  purple: { border: "border-purple-500/30", bg: "bg-purple-500/5", text: "text-purple-400", badge: "bg-purple-500/10 text-purple-400 border-purple-500/20" },
  amber: { border: "border-amber-500/30", bg: "bg-amber-500/5", text: "text-amber-400", badge: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
  cyan: { border: "border-cyan-500/30", bg: "bg-cyan-500/5", text: "text-cyan-400", badge: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20" },
  pink: { border: "border-pink-500/30", bg: "bg-pink-500/5", text: "text-pink-400", badge: "bg-pink-500/10 text-pink-400 border-pink-500/20" },
  orange: { border: "border-orange-500/30", bg: "bg-orange-500/5", text: "text-orange-400", badge: "bg-orange-500/10 text-orange-400 border-orange-500/20" },
  red: { border: "border-red-500/30", bg: "bg-red-500/5", text: "text-red-400", badge: "bg-red-500/10 text-red-400 border-red-500/20" },
};

export default function SystemData() {
  const [activeCategory, setActiveCategory] = useState(0);
  const category = dataCategories[activeCategory];
  const colors = colorMap[category.color];

  const totalRecords = dataCategories.reduce((sum, cat) => sum + cat.count, 0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          System Data
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Complete system data seeded for immediate operation. Myanmar-localized business data
          with realistic products, customers, and suppliers.
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3 mb-10">
        {dataCategories.map((cat) => {
          const c = colorMap[cat.color];
          return (
            <div
              key={cat.name}
              className={`rounded-lg border ${c.border} ${c.bg} p-3 text-center`}
            >
              <div className="text-xl mb-1">{cat.icon}</div>
              <div className={`text-lg font-bold ${c.text}`}>{cat.count}</div>
              <div className="text-[10px] text-gray-500">{cat.name}</div>
            </div>
          );
        })}
      </div>

      {/* Category Selector */}
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        {dataCategories.map((cat, i) => {
          const c = colorMap[cat.color];
          return (
            <button
              key={cat.name}
              onClick={() => setActiveCategory(i)}
              className={`px-3 py-2 rounded-lg text-xs transition-all flex items-center gap-2 ${
                activeCategory === i
                  ? `${c.bg} ${c.border} border ${c.text}`
                  : "bg-gray-900/50 border border-gray-800 text-gray-400 hover:border-gray-700"
              }`}
            >
              <span>{cat.icon}</span>
              <span>{cat.name}</span>
              <span className={`text-[10px] px-1.5 py-0.5 rounded ${c.badge} border`}>
                {cat.count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Category Detail */}
      <div className={`rounded-xl border ${colors.border} ${colors.bg} p-6`}>
        <div className="flex items-center gap-4 mb-6">
          <span className="text-3xl">{category.icon}</span>
          <div>
            <h3 className={`text-xl font-bold ${colors.text}`}>{category.name}</h3>
            <p className="text-xs text-gray-500">{category.count} records</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {category.items.map((item) => (
            <div
              key={item.label}
              className="p-3 rounded-lg bg-gray-950/50 border border-gray-800/50"
            >
              <div className="flex items-center justify-between mb-1">
                <code className="text-[10px] text-gray-500">{item.label}</code>
                <span className={`text-xs font-semibold ${colors.text}`}>{item.value}</span>
              </div>
              {item.detail && (
                <p className="text-[11px] text-gray-500 mt-1">{item.detail}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Admin Credentials */}
      <div className="mt-8 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">🔐</span>
          <div>
            <h4 className="text-lg font-bold text-emerald-400">Admin Credentials</h4>
            <p className="text-xs text-gray-400">Default administrator account for system access</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-3 rounded-lg bg-gray-950/50 border border-gray-800">
            <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Email</div>
            <code className="text-sm text-emerald-400">admin@erp.local</code>
          </div>
          <div className="p-3 rounded-lg bg-gray-950/50 border border-gray-800">
            <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Password</div>
            <code className="text-sm text-emerald-400">Admin@2026!Secure</code>
          </div>
          <div className="p-3 rounded-lg bg-gray-950/50 border border-gray-800">
            <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Role</div>
            <code className="text-sm text-emerald-400">SUPER_ADMIN</code>
          </div>
        </div>
      </div>

      {/* Seed Scripts */}
      <div className="mt-8 rounded-xl border border-gray-800 bg-gray-900/50 p-6">
        <h4 className="text-sm font-semibold text-gray-200 mb-4">
          📜 Seed Scripts
        </h4>
        <div className="space-y-3">
          <div className="p-3 rounded-lg bg-gray-950 border border-gray-800">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-emerald-400 text-xs">python -m</span>
              <code className="text-sm text-gray-300">scripts.seed_data</code>
            </div>
            <p className="text-xs text-gray-500">
              Seeds all system data: permissions, roles, organization, admin user, branches, products, customers, suppliers, and initial stock.
            </p>
          </div>
          <div className="p-3 rounded-lg bg-gray-950 border border-gray-800">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-emerald-400 text-xs">python -m</span>
              <code className="text-sm text-gray-300">scripts.verify_data</code>
            </div>
            <p className="text-xs text-gray-500">
              Verifies all seeded data is present and consistent. Checks record counts, role assignments, and stock integrity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
