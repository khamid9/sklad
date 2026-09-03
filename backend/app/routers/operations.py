from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Batch, InventoryOperation, Product, Sale, User
from app.dependencies.auth import current_user
from app.schemas import BatchIn, BatchOut, QuantityIn, SaleOut
router = APIRouter(tags=['Складские операции'])
def own_product(product_id: int, user: User, db: Session):
    product = db.get(Product, product_id)
    if not product or product.owner_id != user.id: raise HTTPException(404, 'Товар не найден')
    return product
@router.get('/products/{product_id}/batches', response_model=list[BatchOut])
def batches(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    own_product(product_id, user, db); return db.scalars(select(Batch).where(Batch.product_id == product_id).order_by(Batch.created_at.desc())).all()
@router.post('/products/{product_id}/batches', response_model=BatchOut, status_code=201)
def add_batch(product_id: int, data: BatchIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = own_product(product_id, user, db); total = data.boxes * data.items_per_box
    batch = Batch(product_id=product.id, **data.model_dump(), total_quantity=total); product.quantity += total
    db.add_all([batch, InventoryOperation(user_id=user.id, product_id=product.id, operation_type='income', quantity=total, description=f'Добавлена партия {total} шт. {product.name}')]); db.commit(); db.refresh(batch); return batch
@router.get('/batches/{batch_id}', response_model=BatchOut)
def batch(batch_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(Batch, batch_id)
    if not item: raise HTTPException(404, 'Партия не найдена')
    own_product(item.product_id, user, db); return item
@router.delete('/batches/{batch_id}', status_code=204)
def delete_batch(batch_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(Batch, batch_id)
    if not item: raise HTTPException(404, 'Партия не найдена')
    product = own_product(item.product_id, user, db)
    if product.quantity < item.total_quantity: raise HTTPException(400, 'Нельзя удалить партию: часть товара уже продана')
    product.quantity -= item.total_quantity; db.delete(item); db.commit()
@router.post('/inventory/income')
def income(data: QuantityIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = own_product(data.product_id, user, db); product.quantity += data.quantity
    db.add(InventoryOperation(user_id=user.id, product_id=product.id, operation_type='income', quantity=data.quantity, description=f'Добавлено {data.quantity} {product.name}')); db.commit(); return {'product_id': product.id, 'quantity': product.quantity}
@router.post('/sales', response_model=SaleOut, status_code=201)
def sale(data: QuantityIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = db.scalar(select(Product).where(Product.id == data.product_id, Product.owner_id == user.id).with_for_update())
    if not product: raise HTTPException(404, 'Товар не найден')
    if product.quantity < data.quantity: raise HTTPException(400, 'Недостаточно товара на складе')
    product.quantity -= data.quantity; sale = Sale(product_id=product.id, user_id=user.id, quantity=data.quantity, price=product.sale_price, total_amount=product.sale_price * data.quantity)
    db.add_all([sale, InventoryOperation(user_id=user.id, product_id=product.id, operation_type='sale', quantity=data.quantity, description=f'Продано {data.quantity} {product.name}')]); db.commit(); db.refresh(sale); return sale
@router.get('/history')
def history(operation_type: str | None = None, date_from: datetime | None = None, date_to: datetime | None = None, db: Session = Depends(get_db), user: User = Depends(current_user)):
    stmt = select(InventoryOperation).where(InventoryOperation.user_id == user.id)
    if operation_type: stmt = stmt.where(InventoryOperation.operation_type == operation_type)
    if date_from: stmt = stmt.where(InventoryOperation.created_at >= date_from)
    if date_to: stmt = stmt.where(InventoryOperation.created_at <= date_to)
    return db.scalars(stmt.order_by(InventoryOperation.created_at.desc())).all()
def stats_for_period(user_id: int, start: datetime | None, db: Session):
    stmt = select(func.count(Sale.id), func.coalesce(func.sum(Sale.quantity), 0), func.coalesce(func.sum(Sale.total_amount), 0), func.coalesce(func.sum((Sale.price - Product.purchase_price) * Sale.quantity), 0)).join(Product).where(Sale.user_id == user_id)
    if start: stmt = stmt.where(Sale.created_at >= start)
    sales_count, quantity, revenue, profit = db.execute(stmt).one()
    return {'sales_count': sales_count, 'sold_quantity': quantity, 'revenue': float(revenue), 'profit': float(profit)}
@router.get('/dashboard')
def dashboard(db: Session = Depends(get_db), user: User = Depends(current_user)):
    now = datetime.utcnow(); product_count, total_quantity, low_stock_count = db.execute(select(func.count(Product.id), func.coalesce(func.sum(Product.quantity), 0), func.coalesce(func.sum(case((Product.quantity <= Product.min_quantity, 1), else_=0)), 0)).where(Product.owner_id == user.id)).one(); day = stats_for_period(user.id, now - timedelta(days=1), db); week = stats_for_period(user.id, now - timedelta(days=7), db); month = stats_for_period(user.id, now - timedelta(days=30), db)
    return {'total_products': product_count, 'total_quantity': total_quantity, 'sales_today': day['sold_quantity'], 'sales_week': week['sold_quantity'], 'sales_month': month['sold_quantity'], 'revenue_today': day['revenue'], 'revenue_month': month['revenue'], 'profit_today': day['profit'], 'profit_month': month['profit'], 'low_stock_count': low_stock_count}
@router.get('/statistics/{period}')
def statistics(period: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    days = {'day': 1, 'week': 7, 'month': 30}.get(period)
    if not days: raise HTTPException(404, 'Период: day, week или month')
    result = stats_for_period(user.id, datetime.utcnow() - timedelta(days=days), db); result['period'] = period; return result
@router.get('/statistics/top-products')
def top_products(period: str = 'month', db: Session = Depends(get_db), user: User = Depends(current_user)):
    start = {'day': datetime.utcnow()-timedelta(days=1), 'week': datetime.utcnow()-timedelta(days=7), 'month': datetime.utcnow()-timedelta(days=30), 'all': None}.get(period)
    if period not in ('day','week','month','all'): raise HTTPException(400, 'Период: day, week, month или all')
    stmt = select(Product.name, func.sum(Sale.quantity).label('quantity')).join(Sale).where(Sale.user_id == user.id)
    if start: stmt = stmt.where(Sale.created_at >= start)
    return [{'name': name, 'quantity': quantity} for name, quantity in db.execute(stmt.group_by(Product.name).order_by(func.sum(Sale.quantity).desc()).limit(10)).all()]
