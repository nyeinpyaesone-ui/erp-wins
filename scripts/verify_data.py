"""
ERP Platform — System Data Verification Script

Verifies that all system data has been properly seeded and is consistent.
Run: python -m scripts.verify_data
"""

import asyncio
import logging
import sys
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text

from app.infrastructure.database.engine import close_database, get_engine, init_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


async def verify_data() -> bool:
    """Verify all system data is properly seeded."""
    logger.info("=" * 60)
    logger.info("ERP Platform — System Data Verification")
    logger.info("=" * 60)
    
    await init_database()
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            all_passed = True
            
            # 1. Verify permissions
            result = await conn.execute(text("SELECT COUNT(*) FROM permissions"))
            perm_count = result.scalar()
            expected_perms = 47  # Total permissions defined
            if perm_count >= expected_perms:
                logger.info(f"✓ Permissions: {perm_count} (expected >= {expected_perms})")
            else:
                logger.error(f"✗ Permissions: {perm_count} (expected >= {expected_perms})")
                all_passed = False
            
            # 2. Verify roles
            result = await conn.execute(text("SELECT COUNT(*) FROM roles"))
            role_count = result.scalar()
            expected_roles = 7
            if role_count >= expected_roles:
                logger.info(f"✓ Roles: {role_count} (expected >= {expected_roles})")
            else:
                logger.error(f"✗ Roles: {role_count} (expected >= {expected_roles})")
                all_passed = False
            
            # 3. Verify role-permission assignments
            result = await conn.execute(text("SELECT COUNT(*) FROM role_permissions"))
            rp_count = result.scalar()
            if rp_count > 0:
                logger.info(f"✓ Role-permission assignments: {rp_count}")
            else:
                logger.error("✗ No role-permission assignments found")
                all_passed = False
            
            # 4. Verify organization
            result = await conn.execute(
                text("SELECT id, name, code FROM organizations WHERE code = 'DEMO'")
            )
            org = result.fetchone()
            if org:
                logger.info(f"✓ Organization: {org[1]} ({org[2]})")
                tenant_id = org[0]
            else:
                logger.error("✗ Default organization not found")
                all_passed = False
                tenant_id = None
            
            # 5. Verify admin user
            result = await conn.execute(
                text("SELECT id, email, username FROM users WHERE username = 'admin'")
            )
            admin = result.fetchone()
            if admin:
                logger.info(f"✓ Admin user: {admin[1]} ({admin[2]})")
                admin_id = admin[0]
            else:
                logger.error("✗ Admin user not found")
                all_passed = False
                admin_id = None
            
            # 6. Verify admin role assignment
            if admin_id:
                result = await conn.execute(
                    text("""
                        SELECT r.code FROM user_roles ur
                        JOIN roles r ON ur.role_id = r.id
                        WHERE ur.user_id = :user_id
                    """),
                    {"user_id": admin_id},
                )
                admin_roles = [row[0] for row in result.fetchall()]
                if "SUPER_ADMIN" in admin_roles:
                    logger.info(f"✓ Admin role assignment: SUPER_ADMIN")
                else:
                    logger.error(f"✗ Admin role assignment missing SUPER_ADMIN (found: {admin_roles})")
                    all_passed = False
            
            # 7. Verify branches
            result = await conn.execute(
                text("SELECT COUNT(*) FROM branches WHERE tenant_id = :tenant_id"),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            branch_count = result.scalar()
            expected_branches = 4
            if branch_count >= expected_branches:
                logger.info(f"✓ Branches: {branch_count} (expected >= {expected_branches})")
            else:
                logger.error(f"✗ Branches: {branch_count} (expected >= {expected_branches})")
                all_passed = False
            
            # 8. Verify products
            result = await conn.execute(
                text("SELECT COUNT(*) FROM products WHERE tenant_id = :tenant_id"),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            product_count = result.scalar()
            expected_products = 12
            if product_count >= expected_products:
                logger.info(f"✓ Products: {product_count} (expected >= {expected_products})")
            else:
                logger.error(f"✗ Products: {product_count} (expected >= {expected_products})")
                all_passed = False
            
            # 9. Verify customers
            result = await conn.execute(
                text("SELECT COUNT(*) FROM customers WHERE tenant_id = :tenant_id"),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            customer_count = result.scalar()
            expected_customers = 5
            if customer_count >= expected_customers:
                logger.info(f"✓ Customers: {customer_count} (expected >= {expected_customers})")
            else:
                logger.error(f"✗ Customers: {customer_count} (expected >= {expected_customers})")
                all_passed = False
            
            # 10. Verify suppliers
            result = await conn.execute(
                text("SELECT COUNT(*) FROM suppliers WHERE tenant_id = :tenant_id"),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            supplier_count = result.scalar()
            expected_suppliers = 5
            if supplier_count >= expected_suppliers:
                logger.info(f"✓ Suppliers: {supplier_count} (expected >= {expected_suppliers})")
            else:
                logger.error(f"✗ Suppliers: {supplier_count} (expected >= {expected_suppliers})")
                all_passed = False
            
            # 11. Verify stock records
            result = await conn.execute(
                text("SELECT COUNT(*) FROM stocks WHERE tenant_id = :tenant_id"),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            stock_count = result.scalar()
            expected_stock = 48  # 12 products × 4 branches
            if stock_count >= expected_stock:
                logger.info(f"✓ Stock records: {stock_count} (expected >= {expected_stock})")
            else:
                logger.error(f"✗ Stock records: {stock_count} (expected >= {expected_stock})")
                all_passed = False
            
            # 12. Verify stock movements
            result = await conn.execute(
                text("SELECT COUNT(*) FROM stock_movements WHERE tenant_id = :tenant_id"),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            movement_count = result.scalar()
            if movement_count >= expected_stock:
                logger.info(f"✓ Stock movements: {movement_count}")
            else:
                logger.error(f"✗ Stock movements: {movement_count} (expected >= {expected_stock})")
                all_passed = False
            
            # 13. Verify stock consistency (quantity = available + reserved)
            result = await conn.execute(
                text("""
                    SELECT COUNT(*) FROM stocks
                    WHERE tenant_id = :tenant_id
                    AND available_quantity != (quantity - reserved_quantity)
                """),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            inconsistent = result.scalar()
            if inconsistent == 0:
                logger.info("✓ Stock consistency: All records valid")
            else:
                logger.error(f"✗ Stock consistency: {inconsistent} inconsistent records")
                all_passed = False
            
            # 14. Verify total stock value
            result = await conn.execute(
                text("""
                    SELECT 
                        SUM(s.quantity * p.cost_price) as total_cost_value,
                        SUM(s.quantity * p.selling_price) as total_retail_value
                    FROM stocks s
                    JOIN products p ON s.product_id = p.id
                    WHERE s.tenant_id = :tenant_id
                """),
                {"tenant_id": tenant_id} if tenant_id else {},
            )
            row = result.fetchone()
            if row:
                total_cost = row[0] or Decimal("0")
                total_retail = row[1] or Decimal("0")
                logger.info(f"✓ Total inventory cost value: MMK {total_cost:,.2f}")
                logger.info(f"✓ Total inventory retail value: MMK {total_retail:,.2f}")
            
            logger.info("=" * 60)
            if all_passed:
                logger.info("✅ ALL VERIFICATIONS PASSED")
            else:
                logger.error("❌ SOME VERIFICATIONS FAILED")
            logger.info("=" * 60)
            
            return all_passed
    
    finally:
        await close_database()


if __name__ == "__main__":
    result = asyncio.run(verify_data())
    sys.exit(0 if result else 1)
