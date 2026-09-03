from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(120)); email: Mapped[str] = mapped_column(String(255), unique=True, index=True); password_hash: Mapped[str] = mapped_column(String(255)); role: Mapped[str] = mapped_column(String(20), default='user'); is_active: Mapped[bool] = mapped_column(Boolean, default=True); is_approved: Mapped[bool] = mapped_column(Boolean, default=False); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    products = relationship('Product', back_populates='owner', cascade='all, delete-orphan')
class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(100), unique=True); description: Mapped[str | None] = mapped_column(Text, nullable=True); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    products = relationship('Product', back_populates='category')
class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (UniqueConstraint('owner_id', 'article_number', name='uq_product_owner_article'), UniqueConstraint('owner_id', 'barcode', name='uq_product_owner_barcode'), Index('ix_products_owner_created', 'owner_id', 'created_at'), Index('ix_products_owner_category', 'owner_id', 'category_id'))
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(200), index=True); article_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True); barcode: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True); category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'), nullable=True); purchase_price: Mapped[float] = mapped_column(Numeric(12,2), default=0); sale_price: Mapped[float] = mapped_column(Numeric(12,2), default=0); quantity: Mapped[int] = mapped_column(Integer, default=0); min_quantity: Mapped[int] = mapped_column(Integer, default=0); description: Mapped[str | None] = mapped_column(Text, nullable=True); image: Mapped[str | None] = mapped_column(String(500), nullable=True); owner_id: Mapped[int] = mapped_column(ForeignKey('users.id')); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow); updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship('User', back_populates='products'); category = relationship('Category', back_populates='products'); batches = relationship('Batch', back_populates='product', cascade='all, delete-orphan'); sales = relationship('Sale', back_populates='product', cascade='all, delete-orphan')
class Batch(Base):
    __tablename__ = 'batches'
    id: Mapped[int] = mapped_column(primary_key=True); product_id: Mapped[int] = mapped_column(ForeignKey('products.id')); batch_number: Mapped[str | None] = mapped_column(String(100), nullable=True); boxes: Mapped[int] = mapped_column(Integer); items_per_box: Mapped[int] = mapped_column(Integer); total_quantity: Mapped[int] = mapped_column(Integer); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    product = relationship('Product', back_populates='batches')
class Sale(Base):
    __tablename__ = 'sales'
    id: Mapped[int] = mapped_column(primary_key=True); product_id: Mapped[int] = mapped_column(ForeignKey('products.id')); user_id: Mapped[int] = mapped_column(ForeignKey('users.id')); quantity: Mapped[int] = mapped_column(Integer); price: Mapped[float] = mapped_column(Numeric(12,2)); total_amount: Mapped[float] = mapped_column(Numeric(12,2)); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    product = relationship('Product', back_populates='sales')
class InventoryOperation(Base):
    __tablename__ = 'inventory_operations'
    id: Mapped[int] = mapped_column(primary_key=True); user_id: Mapped[int] = mapped_column(ForeignKey('users.id')); product_id: Mapped[int | None] = mapped_column(ForeignKey('products.id'), nullable=True); operation_type: Mapped[str] = mapped_column(String(20)); quantity: Mapped[int] = mapped_column(Integer, default=0); description: Mapped[str] = mapped_column(Text); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
