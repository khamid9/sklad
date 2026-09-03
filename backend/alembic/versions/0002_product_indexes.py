"""Optimize product lookup and scope identifiers per owner."""
from alembic import op

revision = '0002_product_indexes'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("ALTER TABLE products DROP CONSTRAINT IF EXISTS products_article_number_key")
    op.execute("ALTER TABLE products DROP CONSTRAINT IF EXISTS products_barcode_key")
    op.execute("DROP INDEX IF EXISTS ix_products_barcode")
    op.execute("DROP INDEX IF EXISTS products_barcode_key")
    op.execute("DROP INDEX IF EXISTS ix_products_article_number")
    op.execute("DROP INDEX IF EXISTS products_article_number_key")
    op.create_unique_constraint('uq_product_owner_article', 'products', ['owner_id', 'article_number'])
    op.create_unique_constraint('uq_product_owner_barcode', 'products', ['owner_id', 'barcode'])
    op.create_index('ix_products_owner_created', 'products', ['owner_id', 'created_at'])
    op.create_index('ix_products_owner_category', 'products', ['owner_id', 'category_id'])

def downgrade():
    op.drop_index('ix_products_owner_category', table_name='products')
    op.drop_index('ix_products_owner_created', table_name='products')
    op.drop_constraint('uq_product_owner_barcode', 'products', type_='unique')
    op.drop_constraint('uq_product_owner_article', 'products', type_='unique')
    op.create_unique_constraint('products_barcode_key', 'products', ['barcode'])
    op.create_unique_constraint('products_article_number_key', 'products', ['article_number'])