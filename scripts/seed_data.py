"""
ERP Platform — System Data Seed Script

Populates the database with foundational system data:
- System permissions (RBAC)
- System roles (admin, manager, user, etc.)
- Default organization/tenant
- Admin user
- Branches
- Sample products (Myanmar-localized)
- Sample customers
- Sample suppliers
- Initial stock

Run: python -m scripts.seed_data
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.infrastructure.auth.security import hash_password
from app.infrastructure.database.engine import close_database, get_engine, init_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# =============================================================================
# System Permissions
# =============================================================================

SYSTEM_PERMISSIONS = [
    # Users
    ("users", "create", "Create new users"),
    ("users", "read", "View user information"),
    ("users", "update", "Update user information"),
    ("users", "delete", "Delete users"),
    
    # Organizations
    ("organizations", "create", "Create organizations"),
    ("organizations", "read", "View organization information"),
    ("organizations", "update", "Update organization information"),
    ("organizations", "delete", "Delete organizations"),
    
    # Branches
    ("branches", "create", "Create branches"),
    ("branches", "read", "View branch information"),
    ("branches", "update", "Update branch information"),
    ("branches", "delete", "Delete branches"),
    
    # Roles & Permissions
    ("roles", "create", "Create roles"),
    ("roles", "read", "View roles"),
    ("roles", "update", "Update roles"),
    ("roles", "delete", "Delete roles"),
    
    # Products
    ("products", "create", "Create products"),
    ("products", "read", "View products"),
    ("products", "update", "Update products"),
    ("products", "delete", "Delete products"),
    
    # Customers
    ("customers", "create", "Create customers"),
    ("customers", "read", "View customers"),
    ("customers", "update", "Update customers"),
    ("customers", "delete", "Delete customers"),
    
    # Suppliers
    ("suppliers", "create", "Create suppliers"),
    ("suppliers", "read", "View suppliers"),
    ("suppliers", "update", "Update suppliers"),
    ("suppliers", "delete", "Delete suppliers"),
    
    # Inventory
    ("inventory", "create", "Create stock records"),
    ("inventory", "read", "View stock levels"),
    ("inventory", "update", "Adjust stock"),
    ("inventory", "delete", "Delete stock records"),
    
    # Sales
    ("sales", "create", "Create sales orders"),
    ("sales", "read", "View sales orders"),
    ("sales", "update", "Update sales orders"),
    ("sales", "delete", "Delete sales orders"),
    ("sales", "approve", "Approve sales orders"),
    
    # Purchases
    ("purchases", "create", "Create purchase orders"),
    ("purchases", "read", "View purchase orders"),
    ("purchases", "update", "Update purchase orders"),
    ("purchases", "delete", "Delete purchase orders"),
    ("purchases", "approve", "Approve purchase orders"),
    
    # Payments
    ("payments", "create", "Create payments"),
    ("payments", "read", "View payments"),
    ("payments", "update", "Update payments"),
    ("payments", "delete", "Delete payments"),
    ("payments", "approve", "Approve payments"),
    
    # Reports
    ("reports", "read", "View reports"),
    ("reports", "export", "Export reports"),
    
    # Daily Closing
    ("closing", "create", "Perform daily closing"),
    ("closing", "read", "View closing records"),
    ("closing", "approve", "Approve daily closing"),
]


# =============================================================================
# System Roles
# =============================================================================

SYSTEM_ROLES = [
    {
        "code": "SUPER_ADMIN",
        "name": "Super Administrator",
        "description": "Full system access — all permissions across all tenants",
        "is_system": True,
        "permissions": "all",
    },
    {
        "code": "ADMIN",
        "name": "Administrator",
        "description": "Organization-level administration",
        "is_system": True,
        "permissions": [
            "users:create", "users:read", "users:update", "users:delete",
            "organizations:read", "organizations:update",
            "branches:create", "branches:read", "branches:update", "branches:delete",
            "roles:create", "roles:read", "roles:update", "roles:delete",
            "products:create", "products:read", "products:update", "products:delete",
            "customers:create", "customers:read", "customers:update", "customers:delete",
            "suppliers:create", "suppliers:read", "suppliers:update", "suppliers:delete",
            "inventory:create", "inventory:read", "inventory:update", "inventory:delete",
            "sales:create", "sales:read", "sales:update", "sales:delete", "sales:approve",
            "purchases:create", "purchases:read", "purchases:update", "purchases:delete", "purchases:approve",
            "payments:create", "payments:read", "payments:update", "payments:delete", "payments:approve",
            "reports:read", "reports:export",
            "closing:create", "closing:read", "closing:approve",
        ],
    },
    {
        "code": "MANAGER",
        "name": "Branch Manager",
        "description": "Branch-level management with approval authority",
        "is_system": True,
        "permissions": [
            "users:read",
            "branches:read", "branches:update",
            "products:create", "products:read", "products:update",
            "customers:create", "customers:read", "customers:update",
            "suppliers:create", "suppliers:read", "suppliers:update",
            "inventory:create", "inventory:read", "inventory:update",
            "sales:create", "sales:read", "sales:update", "sales:approve",
            "purchases:create", "purchases:read", "purchases:update", "purchases:approve",
            "payments:create", "payments:read", "payments:approve",
            "reports:read", "reports:export",
            "closing:create", "closing:read",
        ],
    },
    {
        "code": "ACCOUNTANT",
        "name": "Accountant",
        "description": "Financial operations and reporting",
        "is_system": True,
        "permissions": [
            "customers:read", "customers:update",
            "suppliers:read", "suppliers:update",
            "inventory:read",
            "sales:read",
            "purchases:read",
            "payments:create", "payments:read", "payments:update", "payments:approve",
            "reports:read", "reports:export",
            "closing:create", "closing:read", "closing:approve",
        ],
    },
    {
        "code": "SALES_PERSON",
        "name": "Sales Person",
        "description": "Sales operations — create and manage sales orders",
        "is_system": True,
        "permissions": [
            "products:read",
            "customers:create", "customers:read", "customers:update",
            "inventory:read",
            "sales:create", "sales:read", "sales:update",
        ],
    },
    {
        "code": "INVENTORY_CLERK",
        "name": "Inventory Clerk",
        "description": "Inventory management — stock movements and adjustments",
        "is_system": True,
        "permissions": [
            "products:read",
            "suppliers:read",
            "inventory:create", "inventory:read", "inventory:update",
            "purchases:read",
        ],
    },
    {
        "code": "VIEWER",
        "name": "Viewer",
        "description": "Read-only access to all modules",
        "is_system": True,
        "permissions": [
            "users:read",
            "organizations:read",
            "branches:read",
            "roles:read",
            "products:read",
            "customers:read",
            "suppliers:read",
            "inventory:read",
            "sales:read",
            "purchases:read",
            "payments:read",
            "reports:read",
            "closing:read",
        ],
    },
]


# =============================================================================
# Default Organization (Tenant)
# =============================================================================

DEFAULT_ORGANIZATION = {
    "id": "00000000-0000-0000-0000-000000000001",
    "code": "DEMO",
    "name": "Demo Trading Company",
    "name_mm": "ဒီမို ကုန်သွယ်ရေး ကုမ္ပဏီ",
    "type": "company",
    "tax_id": "TAX-DEMO-001",
    "address": "No. 123, Pyay Road, Kamayut Township, Yangon, Myanmar",
    "phone": "+95 9 123 456 789",
    "email": "info@demotrading.mm",
}


# =============================================================================
# Admin User
# =============================================================================

ADMIN_USER = {
    "id": "00000000-0000-0000-0000-000000000002",
    "email": "admin@erp.local",
    "username": "admin",
    "password": "Admin@2026!Secure",
    "full_name": "System Administrator",
}


# =============================================================================
# Branches
# =============================================================================

BRANCHES = [
    {
        "id": "00000000-0000-0000-0000-000000000010",
        "code": "HQ",
        "name": "Headquarters",
        "name_mm": "ဌာနချုပ်",
        "type": "headquarters",
        "address": "No. 123, Pyay Road, Kamayut Township, Yangon",
        "phone": "+95 1 123 4567",
    },
    {
        "id": "00000000-0000-0000-0000-000000000011",
        "code": "WH-A",
        "name": "Main Warehouse",
        "name_mm": "အဓိက ကုန်လှောင်ရုံ",
        "type": "warehouse",
        "address": "Industrial Zone, Hlaing Tharyar Township, Yangon",
        "phone": "+95 1 234 5678",
    },
    {
        "id": "00000000-0000-0000-0000-000000000012",
        "code": "RT-01",
        "name": "Downtown Retail Branch",
        "name_mm": "မြို့တွင်း လက်လီဆိုင်",
        "type": "retail",
        "address": "No. 45, Anawrahta Road, Lanmadaw Township, Yangon",
        "phone": "+95 1 345 6789",
    },
    {
        "id": "00000000-0000-0000-0000-000000000013",
        "code": "RT-02",
        "name": "Mandalay Branch",
        "name_mm": "မန္တလေး ဆိုင်ခွဲ",
        "type": "branch",
        "address": "No. 88, 78th Street, Between 36th & 37th Street, Mandalay",
        "phone": "+95 2 123 4567",
    },
]


# =============================================================================
# Products (Myanmar-localized)
# =============================================================================

PRODUCTS = [
    {
        "sku": "RICE-50K",
        "name": "Ponnyasin Rice (50kg)",
        "name_mm": "ပုဏ္ဏသျင် ဆန် (၅၀ ပိဿာ)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000011",
        "cost_price": "45000.00",
        "selling_price": "52000.00",
        "category": "Staples",
    },
    {
        "sku": "OIL-5L",
        "name": "Golden Star Cooking Oil (5L)",
        "name_mm": "ရွှေကြယ် စားအုန်းဆီ (၅ လီတာ)",
        "type": "physical",
        "unit_of_measure": "bottle",
        "barcode": "4810001000028",
        "cost_price": "12000.00",
        "selling_price": "14500.00",
        "category": "Cooking",
    },
    {
        "sku": "SUGAR-10K",
        "name": "White Sugar (10kg)",
        "name_mm": "သကြားဖြူ (၁၀ ကီလို)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000035",
        "cost_price": "15000.00",
        "selling_price": "18000.00",
        "category": "Staples",
    },
    {
        "sku": "SALT-1K",
        "name": "Iodized Salt (1kg)",
        "name_mm": "အိုင်အိုဒင်း ဆား (၁ ကီလို)",
        "type": "physical",
        "unit_of_measure": "pack",
        "barcode": "4810001000042",
        "cost_price": "800.00",
        "selling_price": "1200.00",
        "category": "Staples",
    },
    {
        "sku": "FISHSAUCE-500",
        "name": "Mega Fish Sauce (500ml)",
        "name_mm": "မီဂါ ငါးငံပြာရည် (၅၀၀ မီလီ)",
        "type": "physical",
        "unit_of_measure": "bottle",
        "barcode": "4810001000059",
        "cost_price": "2500.00",
        "selling_price": "3200.00",
        "category": "Condiments",
    },
    {
        "sku": "NOODLE-P5",
        "name": "Mama Instant Noodles (5 pack)",
        "name_mm": "မမ ချက်ချင်းခေါက်ဆွဲ (၅ ပါဆယ်)",
        "type": "physical",
        "unit_of_measure": "pack",
        "barcode": "4810001000066",
        "cost_price": "1500.00",
        "selling_price": "2000.00",
        "category": "Instant Food",
    },
    {
        "sku": "ONION-50K",
        "name": "Shan Onion (50kg)",
        "name_mm": "ရှမ်း ကြက်သွန်နီ (၅၀ ပိဿာ)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000073",
        "cost_price": "25000.00",
        "selling_price": "32000.00",
        "category": "Vegetables",
    },
    {
        "sku": "GARLIC-10K",
        "name": "Shan Garlic (10kg)",
        "name_mm": "ရှမ်း ကြက်သွန်ဖြူ (၁၀ ကီလို)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000080",
        "cost_price": "18000.00",
        "selling_price": "24000.00",
        "category": "Vegetables",
    },
    {
        "sku": "TEA-LB",
        "name": "Shan Tea Leaves (1 viss)",
        "name_mm": "ရှမ်း လက်ဖက် (၁ ပိဿာ)",
        "type": "physical",
        "unit_of_measure": "viss",
        "barcode": "4810001000097",
        "cost_price": "8000.00",
        "selling_price": "11000.00",
        "category": "Beverages",
    },
    {
        "sku": "BEAN-25K",
        "name": "Matpe Bean (25kg)",
        "name_mm": "မတ်ပဲ (၂၅ ကီလို)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000103",
        "cost_price": "22000.00",
        "selling_price": "28000.00",
        "category": "Pulses",
    },
    {
        "sku": "DAL-25K",
        "name": "Red Gram Dal (25kg)",
        "name_mm": "ပဲနီ (၂၅ ကီလို)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000110",
        "cost_price": "28000.00",
        "selling_price": "35000.00",
        "category": "Pulses",
    },
    {
        "sku": "FLOUR-25K",
        "name": "Wheat Flour (25kg)",
        "name_mm": "ဂျုံမှုန့် (၂၅ ကီလို)",
        "type": "physical",
        "unit_of_measure": "bag",
        "barcode": "4810001000127",
        "cost_price": "18000.00",
        "selling_price": "23000.00",
        "category": "Staples",
    },
]


# =============================================================================
# Customers
# =============================================================================

CUSTOMERS = [
    {
        "code": "CUST-001",
        "name": "U Aung Min Trading",
        "name_mm": "ဦးအောင်မင်း ကုန်သွယ်ရေး",
        "type": "business",
        "email": "aungmin.trading@gmail.com",
        "phone": "+95 9 111 222 333",
        "address": "No. 50, Bogyoke Aung San Road, Yangon",
        "tax_id": "CUST-TAX-001",
        "credit_limit": "5000000.00",
    },
    {
        "code": "CUST-002",
        "name": "Daw Khin Marcy Supermarket",
        "name_mm": "ဒေါ်ခင်မာစီ စူပါမားကတ်",
        "type": "business",
        "email": "khinmarcy.super@gmail.com",
        "phone": "+95 9 222 333 444",
        "address": "No. 12, Inya Road, Kamayut, Yangon",
        "tax_id": "CUST-TAX-002",
        "credit_limit": "3000000.00",
    },
    {
        "code": "CUST-003",
        "name": "Ko Zaw Win Retail Shop",
        "name_mm": "ကိုဇော်ဝင်း လက်လီဆိုင်",
        "type": "business",
        "email": "zawwin.shop@gmail.com",
        "phone": "+95 9 333 444 555",
        "address": "No. 8, 35th Street, Mandalay",
        "tax_id": "CUST-TAX-003",
        "credit_limit": "1000000.00",
    },
    {
        "code": "CUST-004",
        "name": "Ma Thida (Walk-in Customer)",
        "name_mm": "မသီတာ",
        "type": "individual",
        "phone": "+95 9 444 555 666",
        "address": "Hlaing Township, Yangon",
        "credit_limit": "200000.00",
    },
    {
        "code": "CUST-005",
        "name": "Myanmar Food Distribution Co.",
        "name_mm": "မြန်မာ အစားအစာ ဖြန့်ဖြူးရေး",
        "type": "business",
        "email": "info@mmfooddist.mm",
        "phone": "+95 1 555 6667",
        "address": "No. 200, Thanlyin Industrial Zone, Yangon",
        "tax_id": "CUST-TAX-005",
        "credit_limit": "10000000.00",
    },
]


# =============================================================================
# Suppliers
# =============================================================================

SUPPLIERS = [
    {
        "code": "SUP-001",
        "name": "Ayeyarwady Rice Mill",
        "name_mm": "ဧရာဝတီ ဆန်စက်",
        "type": "manufacturer",
        "email": "sales@ayeyarwadymill.mm",
        "phone": "+95 42 123 456",
        "address": "Pathein, Ayeyarwady Region",
        "tax_id": "SUP-TAX-001",
        "payment_terms": "Net 30",
        "credit_limit": "20000000.00",
    },
    {
        "code": "SUP-002",
        "name": "Golden Star Oil Factory",
        "name_mm": "ရွှေကြယ် ဆီစက်ရုံ",
        "type": "manufacturer",
        "email": "orders@goldenstaroil.mm",
        "phone": "+95 1 666 7778",
        "address": "Hlaing Tharyar Industrial Zone, Yangon",
        "tax_id": "SUP-TAX-002",
        "payment_terms": "Net 15",
        "credit_limit": "15000000.00",
    },
    {
        "code": "SUP-003",
        "name": "Shan Highland Produce",
        "name_mm": "ရှမ်းတောင်ပေါ် သီးနှံ",
        "type": "distributor",
        "email": "shanhighland@gmail.com",
        "phone": "+95 82 123 456",
        "address": "Taunggyi, Shan State",
        "tax_id": "SUP-TAX-003",
        "payment_terms": "Cash on Delivery",
        "credit_limit": "5000000.00",
    },
    {
        "code": "SUP-004",
        "name": "Mega Condiments Myanmar",
        "name_mm": "မီဂါ အရသာမြန်မာ",
        "type": "manufacturer",
        "email": "sales@megacondiments.mm",
        "phone": "+95 1 777 8889",
        "address": "Shwepyitha Industrial Zone, Yangon",
        "tax_id": "SUP-TAX-004",
        "payment_terms": "Net 30",
        "credit_limit": "8000000.00",
    },
    {
        "code": "SUP-005",
        "name": "Mandalay Pulses & Grains",
        "name_mm": "မန္တလေး ပဲနှင့် ကောက်ပဲသီးနှံ",
        "type": "wholesaler",
        "email": "orders@mdypulses.mm",
        "phone": "+95 2 234 5678",
        "address": "Myitnge Road, Mandalay",
        "tax_id": "SUP-TAX-005",
        "payment_terms": "Net 45",
        "credit_limit": "12000000.00",
    },
]


# =============================================================================
# Initial Stock (per branch)
# =============================================================================

INITIAL_STOCK = {
    "HQ": {
        "RICE-50K": {"quantity": "100", "available": "100"},
        "OIL-5L": {"quantity": "200", "available": "200"},
        "SUGAR-10K": {"quantity": "150", "available": "150"},
        "SALT-1K": {"quantity": "500", "available": "500"},
        "FISHSAUCE-500": {"quantity": "300", "available": "300"},
        "NOODLE-P5": {"quantity": "400", "available": "400"},
        "ONION-50K": {"quantity": "50", "available": "50"},
        "GARLIC-10K": {"quantity": "80", "available": "80"},
        "TEA-LB": {"quantity": "120", "available": "120"},
        "BEAN-25K": {"quantity": "60", "available": "60"},
        "DAL-25K": {"quantity": "40", "available": "40"},
        "FLOUR-25K": {"quantity": "90", "available": "90"},
    },
    "WH-A": {
        "RICE-50K": {"quantity": "1000", "available": "1000"},
        "OIL-5L": {"quantity": "2000", "available": "2000"},
        "SUGAR-10K": {"quantity": "1500", "available": "1500"},
        "SALT-1K": {"quantity": "5000", "available": "5000"},
        "FISHSAUCE-500": {"quantity": "3000", "available": "3000"},
        "NOODLE-P5": {"quantity": "4000", "available": "4000"},
        "ONION-50K": {"quantity": "500", "available": "500"},
        "GARLIC-10K": {"quantity": "800", "available": "800"},
        "TEA-LB": {"quantity": "1200", "available": "1200"},
        "BEAN-25K": {"quantity": "600", "available": "600"},
        "DAL-25K": {"quantity": "400", "available": "400"},
        "FLOUR-25K": {"quantity": "900", "available": "900"},
    },
    "RT-01": {
        "RICE-50K": {"quantity": "30", "available": "30"},
        "OIL-5L": {"quantity": "50", "available": "50"},
        "SUGAR-10K": {"quantity": "40", "available": "40"},
        "SALT-1K": {"quantity": "100", "available": "100"},
        "FISHSAUCE-500": {"quantity": "80", "available": "80"},
        "NOODLE-P5": {"quantity": "150", "available": "150"},
        "ONION-50K": {"quantity": "15", "available": "15"},
        "GARLIC-10K": {"quantity": "20", "available": "20"},
        "TEA-LB": {"quantity": "30", "available": "30"},
        "BEAN-25K": {"quantity": "15", "available": "15"},
        "DAL-25K": {"quantity": "10", "available": "10"},
        "FLOUR-25K": {"quantity": "25", "available": "25"},
    },
    "RT-02": {
        "RICE-50K": {"quantity": "40", "available": "40"},
        "OIL-5L": {"quantity": "60", "available": "60"},
        "SUGAR-10K": {"quantity": "50", "available": "50"},
        "SALT-1K": {"quantity": "120", "available": "120"},
        "FISHSAUCE-500": {"quantity": "100", "available": "100"},
        "NOODLE-P5": {"quantity": "200", "available": "200"},
        "ONION-50K": {"quantity": "20", "available": "20"},
        "GARLIC-10K": {"quantity": "30", "available": "30"},
        "TEA-LB": {"quantity": "40", "available": "40"},
        "BEAN-25K": {"quantity": "20", "available": "20"},
        "DAL-25K": {"quantity": "15", "available": "15"},
        "FLOUR-25K": {"quantity": "35", "available": "35"},
    },
}


# =============================================================================
# Seed Functions
# =============================================================================

async def seed_permissions(session: AsyncSession) -> dict[str, UUID]:
    """Insert system permissions and return mapping."""
    logger.info("Seeding system permissions...")
    
    permission_map: dict[str, UUID] = {}
    now = datetime.now(timezone.utc)
    
    for resource, action, description in SYSTEM_PERMISSIONS:
        perm_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO permissions (id, resource, action, description, created_at)
                VALUES (:id, :resource, :action, :description, :created_at)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": perm_id,
                "resource": resource,
                "action": action,
                "description": description,
                "created_at": now,
            },
        )
        permission_map[f"{resource}:{action}"] = perm_id
    
    await session.commit()
    logger.info(f"  ✓ Created {len(permission_map)} permissions")
    return permission_map


async def seed_roles(
    session: AsyncSession,
    tenant_id: UUID,
    permission_map: dict[str, UUID],
) -> dict[str, UUID]:
    """Insert system roles with permissions."""
    logger.info("Seeding system roles...")
    
    role_map: dict[str, UUID] = {}
    now = datetime.now(timezone.utc)
    
    for role_data in SYSTEM_ROLES:
        role_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO roles (id, name, code, description, is_system, tenant_id, created_at, updated_at)
                VALUES (:id, :name, :code, :description, :is_system, :tenant_id, :created_at, :updated_at)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": role_id,
                "name": role_data["name"],
                "code": role_data["code"],
                "description": role_data["description"],
                "is_system": role_data["is_system"],
                "tenant_id": tenant_id,
                "created_at": now,
                "updated_at": now,
            },
        )
        role_map[role_data["code"]] = role_id
        
        # Assign permissions
        if role_data["permissions"] == "all":
            for perm_id in permission_map.values():
                await session.execute(
                    text("""
                        INSERT INTO role_permissions (role_id, permission_id)
                        VALUES (:role_id, :permission_id)
                        ON CONFLICT DO NOTHING
                    """),
                    {"role_id": role_id, "permission_id": perm_id},
                )
        else:
            for perm_key in role_data["permissions"]:
                if perm_key in permission_map:
                    await session.execute(
                        text("""
                            INSERT INTO role_permissions (role_id, permission_id)
                            VALUES (:role_id, :permission_id)
                            ON CONFLICT DO NOTHING
                        """),
                        {"role_id": role_id, "permission_id": permission_map[perm_key]},
                    )
    
    await session.commit()
    logger.info(f"  ✓ Created {len(role_map)} roles")
    return role_map


async def seed_organization(session: AsyncSession) -> UUID:
    """Insert default organization."""
    logger.info("Seeding default organization...")
    
    org_id = UUID(DEFAULT_ORGANIZATION["id"])
    now = datetime.now(timezone.utc)
    
    await session.execute(
        text("""
            INSERT INTO organizations (id, name, code, type, tax_id, address, phone, email, is_active, created_at, updated_at)
            VALUES (:id, :name, :code, :type, :tax_id, :address, :phone, :email, :is_active, :created_at, :updated_at)
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": org_id,
            "name": DEFAULT_ORGANIZATION["name"],
            "code": DEFAULT_ORGANIZATION["code"],
            "type": DEFAULT_ORGANIZATION["type"],
            "tax_id": DEFAULT_ORGANIZATION["tax_id"],
            "address": DEFAULT_ORGANIZATION["address"],
            "phone": DEFAULT_ORGANIZATION["phone"],
            "email": DEFAULT_ORGANIZATION["email"],
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        },
    )
    
    await session.commit()
    logger.info(f"  ✓ Organization: {DEFAULT_ORGANIZATION['name']} ({DEFAULT_ORGANIZATION['code']})")
    return org_id


async def seed_admin_user(
    session: AsyncSession,
    tenant_id: UUID,
    role_map: dict[str, UUID],
) -> UUID:
    """Insert admin user and assign SUPER_ADMIN role."""
    logger.info("Seeding admin user...")
    
    user_id = UUID(ADMIN_USER["id"])
    now = datetime.now(timezone.utc)
    password_hash = hash_password(ADMIN_USER["password"])
    
    await session.execute(
        text("""
            INSERT INTO users (id, email, username, password_hash, full_name, status, is_active, tenant_id, created_at, updated_at)
            VALUES (:id, :email, :username, :password_hash, :full_name, :status, :is_active, :tenant_id, :created_at, :updated_at)
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": user_id,
            "email": ADMIN_USER["email"],
            "username": ADMIN_USER["username"],
            "password_hash": password_hash,
            "full_name": ADMIN_USER["full_name"],
            "status": "active",
            "is_active": True,
            "tenant_id": tenant_id,
            "created_at": now,
            "updated_at": now,
        },
    )
    
    # Assign SUPER_ADMIN role
    if "SUPER_ADMIN" in role_map:
        await session.execute(
            text("""
                INSERT INTO user_roles (id, user_id, role_id, branch_id, tenant_id, granted_at, granted_by)
                VALUES (:id, :user_id, :role_id, NULL, :tenant_id, :granted_at, :granted_by)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": uuid4(),
                "user_id": user_id,
                "role_id": role_map["SUPER_ADMIN"],
                "tenant_id": tenant_id,
                "granted_at": now,
                "granted_by": user_id,
            },
        )
    
    await session.commit()
    logger.info(f"  ✓ Admin user: {ADMIN_USER['email']}")
    return user_id


async def seed_branches(
    session: AsyncSession,
    tenant_id: UUID,
) -> dict[str, UUID]:
    """Insert branches."""
    logger.info("Seeding branches...")
    
    branch_map: dict[str, UUID] = {}
    now = datetime.now(timezone.utc)
    org_id = UUID(DEFAULT_ORGANIZATION["id"])
    
    for branch_data in BRANCHES:
        branch_id = UUID(branch_data["id"])
        await session.execute(
            text("""
                INSERT INTO branches (id, organization_id, name, code, type, address, phone, email, is_active, tenant_id, created_at, updated_at)
                VALUES (:id, :organization_id, :name, :code, :type, :address, :phone, :email, :is_active, :tenant_id, :created_at, :updated_at)
                ON CONFLICT (id) DO NOTHING
            """),
            {
                "id": branch_id,
                "organization_id": org_id,
                "name": branch_data["name"],
                "code": branch_data["code"],
                "type": branch_data["type"],
                "address": branch_data["address"],
                "phone": branch_data["phone"],
                "email": None,
                "is_active": True,
                "tenant_id": tenant_id,
                "created_at": now,
                "updated_at": now,
            },
        )
        branch_map[branch_data["code"]] = branch_id
    
    await session.commit()
    logger.info(f"  ✓ Created {len(branch_map)} branches")
    return branch_map


async def seed_products(
    session: AsyncSession,
    tenant_id: UUID,
) -> dict[str, UUID]:
    """Insert products."""
    logger.info("Seeding products...")
    
    product_map: dict[str, UUID] = {}
    now = datetime.now(timezone.utc)
    
    for product_data in PRODUCTS:
        product_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO products (id, sku, name, description, type, status, unit_of_measure, barcode, cost_price, selling_price, is_trackable, tenant_id, created_at, updated_at)
                VALUES (:id, :sku, :name, :description, :type, :status, :unit_of_measure, :barcode, :cost_price, :selling_price, :is_trackable, :tenant_id, :created_at, :updated_at)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": product_id,
                "sku": product_data["sku"],
                "name": product_data["name"],
                "description": product_data.get("name_mm", ""),
                "type": product_data["type"],
                "status": "active",
                "unit_of_measure": product_data["unit_of_measure"],
                "barcode": product_data["barcode"],
                "cost_price": Decimal(product_data["cost_price"]),
                "selling_price": Decimal(product_data["selling_price"]),
                "is_trackable": True,
                "tenant_id": tenant_id,
                "created_at": now,
                "updated_at": now,
            },
        )
        product_map[product_data["sku"]] = product_id
    
    await session.commit()
    logger.info(f"  ✓ Created {len(product_map)} products")
    return product_map


async def seed_customers(
    session: AsyncSession,
    tenant_id: UUID,
) -> dict[str, UUID]:
    """Insert customers."""
    logger.info("Seeding customers...")
    
    customer_map: dict[str, UUID] = {}
    now = datetime.now(timezone.utc)
    
    for customer_data in CUSTOMERS:
        customer_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO customers (id, code, name, type, status, email, phone, address, tax_id, credit_limit, current_balance, notes, tenant_id, created_at, updated_at)
                VALUES (:id, :code, :name, :type, :status, :email, :phone, :address, :tax_id, :credit_limit, :current_balance, :notes, :tenant_id, :created_at, :updated_at)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": customer_id,
                "code": customer_data["code"],
                "name": customer_data["name"],
                "type": customer_data["type"],
                "status": "active",
                "email": customer_data.get("email"),
                "phone": customer_data.get("phone"),
                "address": customer_data.get("address"),
                "tax_id": customer_data.get("tax_id"),
                "credit_limit": Decimal(customer_data["credit_limit"]),
                "current_balance": Decimal("0"),
                "notes": customer_data.get("name_mm", ""),
                "tenant_id": tenant_id,
                "created_at": now,
                "updated_at": now,
            },
        )
        customer_map[customer_data["code"]] = customer_id
    
    await session.commit()
    logger.info(f"  ✓ Created {len(customer_map)} customers")
    return customer_map


async def seed_suppliers(
    session: AsyncSession,
    tenant_id: UUID,
) -> dict[str, UUID]:
    """Insert suppliers."""
    logger.info("Seeding suppliers...")
    
    supplier_map: dict[str, UUID] = {}
    now = datetime.now(timezone.utc)
    
    for supplier_data in SUPPLIERS:
        supplier_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO suppliers (id, code, name, type, status, email, phone, address, tax_id, payment_terms, credit_limit, current_balance, notes, tenant_id, created_at, updated_at)
                VALUES (:id, :code, :name, :type, :status, :email, :phone, :address, :tax_id, :payment_terms, :credit_limit, :current_balance, :notes, :tenant_id, :created_at, :updated_at)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": supplier_id,
                "code": supplier_data["code"],
                "name": supplier_data["name"],
                "type": supplier_data["type"],
                "status": "active",
                "email": supplier_data.get("email"),
                "phone": supplier_data.get("phone"),
                "address": supplier_data.get("address"),
                "tax_id": supplier_data.get("tax_id"),
                "payment_terms": supplier_data.get("payment_terms"),
                "credit_limit": Decimal(supplier_data["credit_limit"]),
                "current_balance": Decimal("0"),
                "notes": supplier_data.get("name_mm", ""),
                "tenant_id": tenant_id,
                "created_at": now,
                "updated_at": now,
            },
        )
        supplier_map[supplier_data["code"]] = supplier_id
    
    await session.commit()
    logger.info(f"  ✓ Created {len(supplier_map)} suppliers")
    return supplier_map


async def seed_initial_stock(
    session: AsyncSession,
    tenant_id: UUID,
    product_map: dict[str, UUID],
    branch_map: dict[str, UUID],
    admin_user_id: UUID,
) -> int:
    """Insert initial stock for all products at all branches."""
    logger.info("Seeding initial stock...")
    
    count = 0
    now = datetime.now(timezone.utc)
    
    for branch_code, stock_data in INITIAL_STOCK.items():
        if branch_code not in branch_map:
            logger.warning(f"  ⚠ Branch {branch_code} not found, skipping")
            continue
        
        branch_id = branch_map[branch_code]
        
        for sku, stock_info in stock_data.items():
            if sku not in product_map:
                logger.warning(f"  ⚠ Product {sku} not found, skipping")
                continue
            
            product_id = product_map[sku]
            stock_id = uuid4()
            quantity = Decimal(stock_info["quantity"])
            
            # Get product unit
            product = PRODUCTS[[p["sku"] for p in PRODUCTS].index(sku)]
            uom = product["unit_of_measure"]
            
            # Create stock record
            await session.execute(
                text("""
                    INSERT INTO stocks (id, product_id, branch_id, quantity, reserved_quantity, available_quantity, unit_of_measure, status, tenant_id, created_at, updated_at)
                    VALUES (:id, :product_id, :branch_id, :quantity, :reserved, :available, :uom, :status, :tenant_id, :created_at, :updated_at)
                    ON CONFLICT DO NOTHING
                """),
                {
                    "id": stock_id,
                    "product_id": product_id,
                    "branch_id": branch_id,
                    "quantity": quantity,
                    "reserved": Decimal("0"),
                    "available": quantity,
                    "uom": uom,
                    "status": "available",
                    "tenant_id": tenant_id,
                    "created_at": now,
                    "updated_at": now,
                },
            )
            
            # Create initial receipt movement
            await session.execute(
                text("""
                    INSERT INTO stock_movements (id, product_id, branch_id, movement_type, quantity, reference_type, reference_id, notes, performed_by, tenant_id, created_at)
                    VALUES (:id, :product_id, :branch_id, :movement_type, :quantity, :reference_type, NULL, :notes, :performed_by, :tenant_id, :created_at)
                """),
                {
                    "id": uuid4(),
                    "product_id": product_id,
                    "branch_id": branch_id,
                    "movement_type": "receipt",
                    "quantity": quantity,
                    "reference_type": "seed_data",
                    "notes": f"Initial stock seed for {branch_code}",
                    "performed_by": admin_user_id,
                    "tenant_id": tenant_id,
                    "created_at": now,
                },
            )
            
            count += 1
    
    await session.commit()
    logger.info(f"  ✓ Created {count} stock records with movement history")
    return count


# =============================================================================
# Main Seed Function
# =============================================================================

async def seed_all() -> None:
    """Run all seed operations."""
    logger.info("=" * 60)
    logger.info("ERP Platform — System Data Seeding")
    logger.info("=" * 60)
    
    await init_database()
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            # Use the connection as a session
            from sqlalchemy.ext.asyncio import AsyncSession
            session = AsyncSession(conn)
            
            # 1. Seed permissions
            permission_map = await seed_permissions(session)
            
            # 2. Seed organization
            tenant_id = await seed_organization(session)
            
            # 3. Seed roles (with permissions)
            role_map = await seed_roles(session, tenant_id, permission_map)
            
            # 4. Seed admin user
            admin_user_id = await seed_admin_user(session, tenant_id, role_map)
            
            # 5. Seed branches
            branch_map = await seed_branches(session, tenant_id)
            
            # 6. Seed products
            product_map = await seed_products(session, tenant_id)
            
            # 7. Seed customers
            customer_map = await seed_customers(session, tenant_id)
            
            # 8. Seed suppliers
            supplier_map = await seed_suppliers(session, tenant_id)
            
            # 9. Seed initial stock
            stock_count = await seed_initial_stock(
                session, tenant_id, product_map, branch_map, admin_user_id
            )
        
        logger.info("=" * 60)
        logger.info("✅ System data seeding completed successfully!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Summary:")
        logger.info(f"  • Permissions: {len(permission_map)}")
        logger.info(f"  • Roles: {len(role_map)}")
        logger.info(f"  • Organization: {DEFAULT_ORGANIZATION['name']}")
        logger.info(f"  • Admin user: {ADMIN_USER['email']}")
        logger.info(f"  • Branches: {len(branch_map)}")
        logger.info(f"  • Products: {len(product_map)}")
        logger.info(f"  • Customers: {len(customer_map)}")
        logger.info(f"  • Suppliers: {len(supplier_map)}")
        logger.info(f"  • Stock records: {stock_count}")
        logger.info("")
        logger.info("Login credentials:")
        logger.info(f"  Email: {ADMIN_USER['email']}")
        logger.info(f"  Password: {ADMIN_USER['password']}")
        logger.info(f"  Tenant ID: {tenant_id}")
        logger.info("")
    
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(seed_all())
