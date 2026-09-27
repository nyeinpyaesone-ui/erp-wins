"""Create transaction tables

Revision ID: 003_transactions
Revises: 002_core_business
Create Date: 2026-01-15 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003_transactions'
down_revision: Union[str, None] = '002_core_business'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Sales orders table
    op.create_table(
        'sales_orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('order_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('customers.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('order_date', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('status', sa.String(20), default='draft', nullable=False, index=True),
        sa.Column('subtotal', sa.Numeric(15, 2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('discount_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('total_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('payment_status', sa.String(20), default='pending', nullable=False, index=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Sales order items table
    op.create_table(
        'sales_order_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('sales_order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sales_orders.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('quantity', sa.Numeric(15, 4), nullable=False),
        sa.Column('unit_price', sa.Numeric(15, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('line_total', sa.Numeric(15, 2), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Purchase orders table
    op.create_table(
        'purchase_orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('order_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('supplier_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('suppliers.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('order_date', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('status', sa.String(20), default='draft', nullable=False, index=True),
        sa.Column('subtotal', sa.Numeric(15, 2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('discount_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('total_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('payment_status', sa.String(20), default='pending', nullable=False, index=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Purchase order items table
    op.create_table(
        'purchase_order_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('purchase_order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('purchase_orders.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('quantity', sa.Numeric(15, 4), nullable=False),
        sa.Column('unit_price', sa.Numeric(15, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('line_total', sa.Numeric(15, 2), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Payments table
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('payment_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('payment_type', sa.String(20), nullable=False, index=True),
        sa.Column('payment_method', sa.String(20), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('payment_date', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('status', sa.String(20), default='pending', nullable=False, index=True),
        sa.Column('reference_number', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Payment allocations table
    op.create_table(
        'payment_allocations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('invoice_type', sa.String(20), nullable=False, index=True),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('allocated_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Receivables table
    op.create_table(
        'receivables',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('receivable_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('customers.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('sales_order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sales_orders.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('issue_date', sa.Date(), nullable=False, index=True),
        sa.Column('due_date', sa.Date(), nullable=False, index=True),
        sa.Column('total_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('outstanding_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('status', sa.String(20), default='open', nullable=False, index=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Receivable payments table
    op.create_table(
        'receivable_payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('receivable_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('receivables.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('applied_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('applied_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Payables table
    op.create_table(
        'payables',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('payable_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('supplier_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('suppliers.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('purchase_order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('purchase_orders.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('issue_date', sa.Date(), nullable=False, index=True),
        sa.Column('due_date', sa.Date(), nullable=False, index=True),
        sa.Column('total_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('outstanding_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('status', sa.String(20), default='open', nullable=False, index=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Payable payments table
    op.create_table(
        'payable_payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('payable_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payables.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('payments.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('applied_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('applied_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Daily closings table
    op.create_table(
        'daily_closings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('closing_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('closing_date', sa.Date(), nullable=False, index=True),
        sa.Column('status', sa.String(20), default='draft', nullable=False, index=True),
        sa.Column('total_sales', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('sales_count', sa.Integer(), default=0, nullable=False),
        sa.Column('total_purchases', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('purchase_count', sa.Integer(), default=0, nullable=False),
        sa.Column('total_customer_payments', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('customer_payment_count', sa.Integer(), default=0, nullable=False),
        sa.Column('total_supplier_payments', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('supplier_payment_count', sa.Integer(), default=0, nullable=False),
        sa.Column('opening_cash', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('closing_cash', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('expected_cash', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('cash_difference', sa.Numeric(15, 2), default=0, nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('daily_closings')
    op.drop_table('payable_payments')
    op.drop_table('payables')
    op.drop_table('receivable_payments')
    op.drop_table('receivables')
    op.drop_table('payment_allocations')
    op.drop_table('payments')
    op.drop_table('purchase_order_items')
    op.drop_table('purchase_orders')
    op.drop_table('sales_order_items')
    op.drop_table('sales_orders')
