from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Batch, Category, InventoryOperation, Product, Sale, User
from app.dependencies.auth import current_user
from app.schemas import CategoryIn, CategoryOut, ProductIn, ProductOut, ProductPage
router = APIRouter(tags=['Товары и категории'])
def product_or_404(product_id: int, user: User, db: Session) -> Product:
    product = db.get(Product, product_id)
    if not product or (product.owner_id != user.id and user.role != 'admin'): raise HTTPException(404, 'Товар не найден')
    return product
@router.get('/categories', response_model=list[CategoryOut])
def categories(db: Session = Depends(get_db), _: User = Depends(current_user)): return db.scalars(select(Category).order_by(Category.name)).all()
@router.post('/categories', response_model=CategoryOut, status_code=201)
def create_category(data: CategoryIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    category = Category(**data.model_dump()); db.add(category)
    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(409, 'Категория с таким названием уже существует')
    db.refresh(category); return category
@router.get('/categories/{category_id}', response_model=CategoryOut)
def category(category_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    item = db.get(Category, category_id)
    if not item: raise HTTPException(404, 'Категория не найдена')
    return item
@router.put('/categories/{category_id}', response_model=CategoryOut)
def update_category(category_id: int, data: CategoryIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    item = db.get(Category, category_id)
    if not item: raise HTTPException(404, 'Категория не найдена')
    for key, value in data.model_dump().items(): setattr(item, key, value)
    db.commit(); db.refresh(item); return item
@router.delete('/categories/{category_id}', status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    item = db.get(Category, category_id)
    if not item: raise HTTPException(404, 'Категория не найдена')
    db.delete(item); db.commit()
@router.get('/products', response_model=ProductPage)
def products(search: str | None = None, category_id: int | None = None, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db), user: User = Depends(current_user)):
    stmt = select(Product).where(Product.owner_id == user.id)
    if search:
        search_conditions = [Product.name.ilike(f'%{search}%'), Product.article_number.ilike(f'%{search}%'), Product.barcode.ilike(f'%{search}%')]
        if search.isdigit(): search_conditions.append(Product.id == int(search))
        stmt = stmt.where(or_(*search_conditions))
    if category_id: stmt = stmt.where(Product.category_id == category_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.order_by(Product.created_at.desc()).offset(offset).limit(limit)).all()
    return {'items': items, 'total': total, 'limit': limit, 'offset': offset}
@router.post('/products', response_model=ProductOut, status_code=201)
def create_product(data: ProductIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = Product(**data.model_dump(), owner_id=user.id); db.add(product)
    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(409, 'Артикул или штрих-код уже используется')
    db.refresh(product); return product
@router.get('/products/low-stock', response_model=list[ProductOut])
def low_stock(db: Session = Depends(get_db), user: User = Depends(current_user)): return db.scalars(select(Product).where(Product.owner_id == user.id, Product.quantity <= Product.min_quantity)).all()
@router.get('/products/barcode/{barcode}', response_model=ProductOut)
def by_barcode(barcode: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = db.scalar(select(Product).where(Product.owner_id == user.id, Product.barcode == barcode))
    if not product: raise HTTPException(404, 'Товар не найден')
    return product
@router.get('/products/{product_id}', response_model=ProductOut)
def product(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)): return product_or_404(product_id, user, db)
@router.put('/products/{product_id}', response_model=ProductOut)
def update_product(product_id: int, data: ProductIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = product_or_404(product_id, user, db)
    for key, value in data.model_dump().items(): setattr(product, key, value)
    db.add(InventoryOperation(user_id=user.id, product_id=product.id, operation_type='update', description=f'Изменён товар {product.name}'))
    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(409, 'Артикул или штрих-код уже используется')
    db.refresh(product); return product
@router.delete('/products/{product_id}', status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    product = product_or_404(product_id, user, db)
    if db.scalar(select(Sale.id).where(Sale.product_id == product.id).limit(1)) or db.scalar(select(Batch.id).where(Batch.product_id == product.id).limit(1)):
        raise HTTPException(409, 'Нельзя удалить товар с историей операций. Обнулите остаток или скройте его.')
    db.add(InventoryOperation(user_id=user.id, product_id=None, operation_type='delete', description=f'Удалён товар {product.name}')); db.delete(product); db.commit()
