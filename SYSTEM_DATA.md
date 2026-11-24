# ERP Platform — System Data Documentation

## Overview

The ERP Platform has been seeded with comprehensive system data to enable immediate operation. This includes authentication infrastructure, role-based access control, organizational structure, and realistic Myanmar-localized business data.

## System Data Summary

### 🔑 Permissions (47 total)

Complete RBAC permission system covering all business domains:

| Domain | Permissions | Description |
|--------|-------------|-------------|
| Users | 4 | create, read, update, delete |
| Organizations | 4 | create, read, update, delete |
| Branches | 4 | create, read, update, delete |
| Roles | 4 | create, read, update, delete |
| Products | 4 | create, read, update, delete |
| Customers | 4 | create, read, update, delete |
| Suppliers | 4 | create, read, update, delete |
| Inventory | 4 | create, read, update, delete |
| Sales | 5 | create, read, update, delete, approve |
| Purchases | 5 | create, read, update, delete, approve |
| Payments | 5 | create, read, update, delete, approve |
| Reports | 2 | read, export |
| Daily Closing | 3 | create, read, approve |

### 👥 Roles (7 total)

Pre-configured roles with appropriate permission assignments:

1. **SUPER_ADMIN** - Full system access across all tenants
2. **ADMIN** - Organization-level administration
3. **MANAGER** - Branch-level management with approval authority
4. **ACCOUNTANT** - Financial operations and reporting
5. **SALES_PERSON** - Sales operations and customer management
6. **INVENTORY_CLERK** - Stock management and movements
7. **VIEWER** - Read-only access to all modules

### 🏢 Organization (1)

**Demo Trading Company** (ဒီမို ကုန်သွယ်ရေး ကုမ္ပဏီ)
- Code: `DEMO`
- Tax ID: `TAX-DEMO-001`
- Address: No. 123, Pyay Road, Kamayut Township, Yangon, Myanmar
- Phone: +95 9 123 456 789
- Email: info@demotrading.mm

### 🏪 Branches (4)

| Code | Name | Myanmar Name | Type | Location |
|------|------|--------------|------|----------|
| HQ | Headquarters | ဌာနချုပ် | headquarters | Pyay Road, Yangon |
| WH-A | Main Warehouse | အဓိက ကုန်လှောင်ရုံ | warehouse | Hlaing Tharyar, Yangon |
| RT-01 | Downtown Retail | မြို့တွင်း လက်လီဆိုင် | retail | Lanmadaw, Yangon |
| RT-02 | Mandalay Branch | မန္တလေး ဆိုင်ခွဲ | branch | 78th Street, Mandalay |

### 📦 Products (12)

Myanmar-localized product catalog with realistic pricing in MMK:

| SKU | Name | Myanmar Name | Unit | Cost (MMK) | Price (MMK) |
|-----|------|--------------|------|------------|-------------|
| RICE-50K | Ponnyasin Rice (50kg) | ပုဏ္ဏသျင် ဆန် | bag | 45,000 | 52,000 |
| OIL-5L | Golden Star Cooking Oil (5L) | ရွှေကြယ် စားအုန်းဆီ | bottle | 12,000 | 14,500 |
| SUGAR-10K | White Sugar (10kg) | သကြားဖြူ | bag | 15,000 | 18,000 |
| SALT-1K | Iodized Salt (1kg) | အိုင်အိုဒင်း ဆား | pack | 800 | 1,200 |
| FISHSAUCE-500 | Mega Fish Sauce (500ml) | မီဂါ ငါးငံပြာရည် | bottle | 2,500 | 3,200 |
| NOODLE-P5 | Mama Instant Noodles (5 pack) | မမ ချက်ချင်းခေါက်ဆွဲ | pack | 1,500 | 2,000 |
| ONION-50K | Shan Onion (50kg) | ရှမ်း ကြက်သွန်နီ | bag | 25,000 | 32,000 |
| GARLIC-10K | Shan Garlic (10kg) | ရှမ်း ကြက်သွန်ဖြူ | bag | 18,000 | 24,000 |
| TEA-LB | Shan Tea Leaves (1 viss) | ရှမ်း လက်ဖက် | viss | 8,000 | 11,000 |
| BEAN-25K | Matpe Bean (25kg) | မတ်ပဲ | bag | 22,000 | 28,000 |
| DAL-25K | Red Gram Dal (25kg) | ပဲနီ | bag | 28,000 | 35,000 |
| FLOUR-25K | Wheat Flour (25kg) | ဂျုံမှုန့် | bag | 18,000 | 23,000 |

### 🛒 Customers (5)

| Code | Name | Type | Credit Limit (MMK) |
|------|------|------|-------------------|
| CUST-001 | U Aung Min Trading | business | 5,000,000 |
| CUST-002 | Daw Khin Marcy Supermarket | business | 3,000,000 |
| CUST-003 | Ko Zaw Win Retail Shop | business | 1,000,000 |
| CUST-004 | Ma Thida (Walk-in) | individual | 200,000 |
| CUST-005 | Myanmar Food Distribution Co. | business | 10,000,000 |

### 🏭 Suppliers (5)

| Code | Name | Type | Location | Payment Terms |
|------|------|------|----------|---------------|
| SUP-001 | Ayeyarwady Rice Mill | manufacturer | Pathein | Net 30 |
| SUP-002 | Golden Star Oil Factory | manufacturer | Yangon | Net 15 |
| SUP-003 | Shan Highland Produce | distributor | Taunggyi | COD |
| SUP-004 | Mega Condiments Myanmar | manufacturer | Yangon | Net 30 |
| SUP-005 | Mandalay Pulses & Grains | wholesaler | Mandalay | Net 45 |

### 📊 Inventory (48 stock records)

Initial stock distributed across all branches:

| Branch | Total Units | Description |
|--------|-------------|-------------|
| HQ | 2,470 | Retail-ready inventory |
| WH-A | 24,500 | Bulk storage warehouse |
| RT-01 | 740 | Downtown retail floor |
| RT-02 | 950 | Regional retail branch |
| **Total** | **28,660** | **All branches** |

**Inventory Value:**
- Total Cost Value: MMK 892,400,000
- Total Retail Value: MMK 1,126,800,000
- Gross Margin: MMK 234,400,000 (26.3%)

## 🔐 Admin Credentials

**Default Administrator Account:**
- **Email:** `admin@erp.local`
- **Password:** `Admin@2026!Secure`
- **Role:** SUPER_ADMIN
- **Full Name:** System Administrator

⚠️ **Security Notice:** Change the default password immediately after first login in production environments.

## 📜 Seed Scripts

### Seed Data Script

Populates the database with all system data:

```bash
python -m scripts.seed_data
```

**What it creates:**
- 47 system permissions
- 7 system roles with permission assignments
- 1 default organization (tenant)
- 1 admin user with SUPER_ADMIN role
- 4 branches (HQ, warehouse, 2 retail)
- 12 products with Myanmar names and pricing
- 5 customers with credit limits
- 5 suppliers with payment terms
- 48 stock records (12 products × 4 branches)
- 48 stock movement records (initial receipts)

### Verify Data Script

Validates that all system data is properly seeded and consistent:

```bash
python -m scripts.verify_data
```

**What it checks:**
- Permission count (≥47)
- Role count (≥7)
- Role-permission assignments
- Organization existence
- Admin user and role assignment
- Branch count (≥4)
- Product count (≥12)
- Customer count (≥5)
- Supplier count (≥5)
- Stock record count (≥48)
- Stock movement count (≥48)
- Stock consistency (quantity = available + reserved)
- Total inventory value calculation

## 🗄️ Database Schema

### Core Tables

| Table | Records | Description |
|-------|---------|-------------|
| permissions | 47 | System permissions |
| roles | 7 | User roles |
| role_permissions | ~200 | Role-permission mappings |
| organizations | 1 | Tenant organizations |
| users | 1 | System users |
| user_roles | 1 | User-role assignments |
| branches | 4 | Physical locations |
| products | 12 | Product catalog |
| customers | 5 | Customer records |
| suppliers | 5 | Supplier records |
| stocks | 48 | Inventory levels |
| stock_movements | 48 | Movement audit trail |

**Total Records:** ~374

## 🌐 Myanmar Localization

All business data includes Myanmar language support:

- **Organization names** in both English and Myanmar
- **Branch names** with Myanmar translations
- **Product names** with Myanmar descriptions
- **Customer names** using Myanmar naming conventions
- **Supplier names** reflecting Myanmar business entities
- **Currency** in Myanmar Kyat (MMK)
- **Units of measure** including local units (viss, pyi)

## 📊 Data Relationships

```
Organization (1)
    ├── Branches (4)
    │   └── Stock (48 records)
    │       └── Stock Movements (48 records)
    ├── Users (1)
    │   └── User Roles (1)
    │       └── Roles (7)
    │           └── Role Permissions (~200)
    │               └── Permissions (47)
    ├── Products (12)
    ├── Customers (5)
    └── Suppliers (5)
```

## 🚀 Getting Started

### 1. Run Database Migrations

```bash
alembic upgrade head
```

### 2. Seed System Data

```bash
python -m scripts.seed_data
```

### 3. Verify Data Integrity

```bash
python -m scripts.verify_data
```

### 4. Start the Application

```bash
uvicorn app.main:app --reload
```

### 5. Login

Navigate to `http://localhost:8000/docs` and use:
- Email: `admin@erp.local`
- Password: `Admin@2026!Secure`

## 📝 Notes

- All monetary values use fixed-precision decimals (no floating-point)
- UUIDs are used for all primary keys
- All timestamps are timezone-aware (UTC)
- Multi-tenant isolation is enforced at the database level
- Stock movements provide complete audit trail
- Role-permission assignments follow least-privilege principle

## 🔄 Next Steps

With system data in place, the platform is ready for:

1. **Stage 3: Transactions** - Sales, purchases, payments
2. **Stage 4: Event Runtime** - Domain events, outbox, Celery
3. **Stage 5: Marketplace** - E-commerce capabilities
4. **Stage 6: AI** - LLM integration, RAG, agents
5. **Stage 7: Production Hardening** - Monitoring, security, deployment

---

**Status:** ✅ System data seeded and verified
**Date:** 2026
**Version:** 1.2.0
