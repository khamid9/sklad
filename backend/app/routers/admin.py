from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Batch, InventoryOperation, Product, Sale, User
from app.dependencies.auth import admin_user
router = APIRouter(prefix='/admin', tags=['Администрирование'])
@router.get('/users')
def users(db: Session = Depends(get_db), _: User = Depends(admin_user)): return db.scalars(select(User).order_by(User.created_at.desc())).all()
@router.get('/users/{user_id}')
def user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_user)):
    item = db.get(User, user_id)
    if not item: raise HTTPException(404, 'Пользователь не найден')
    return item
@router.patch('/users/{user_id}/approve')
def approve_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_user)):
    item = db.get(User, user_id)
    if not item: raise HTTPException(404, 'Пользователь не найден')
    item.is_approved = True; item.is_active = True; db.commit(); return {'id': item.id, 'is_approved': True, 'is_active': True}
@router.patch('/users/{user_id}/block')
def block_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(admin_user)):
    item = db.get(User, user_id)
    if not item: raise HTTPException(404, 'Пользователь не найден')
    if item.id == admin.id: raise HTTPException(400, 'Нельзя заблокировать себя')
    item.is_active = not item.is_active; db.commit(); return {'id': item.id, 'is_active': item.is_active}
@router.delete('/users/{user_id}', status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(admin_user)):
    item = db.get(User, user_id)
    if not item: raise HTTPException(404, 'Пользователь не найден')
    if item.id == admin.id: raise HTTPException(400, 'Нельзя удалить себя')
    product_ids = select(Product.id).where(Product.owner_id == item.id)
    db.execute(delete(InventoryOperation).where((InventoryOperation.user_id == item.id) | InventoryOperation.product_id.in_(product_ids)))
    db.execute(delete(Sale).where((Sale.user_id == item.id) | Sale.product_id.in_(product_ids)))
    db.execute(delete(Batch).where(Batch.product_id.in_(product_ids)))
    db.execute(delete(Product).where(Product.owner_id == item.id))
    db.delete(item); db.commit()
@router.get('/products')
def products(db: Session = Depends(get_db), _: User = Depends(admin_user)): return db.scalars(select(Product).order_by(Product.created_at.desc())).all()
@router.get('/statistics')
def statistics(db: Session = Depends(get_db), _: User = Depends(admin_user)):
    revenue = db.scalar(select(func.coalesce(func.sum(Sale.total_amount), 0)))
    profit = db.scalar(select(func.coalesce(func.sum((Sale.price - Product.purchase_price) * Sale.quantity), 0)).join(Product))
    return {'users_count': db.scalar(select(func.count(User.id))), 'products_count': db.scalar(select(func.count(Product.id))), 'sales_count': db.scalar(select(func.count(Sale.id))), 'revenue': float(revenue), 'profit': float(profit)}
