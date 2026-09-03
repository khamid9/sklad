from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings
from app.database.database import get_db
from app.database.models import User
from app.dependencies.auth import current_user
from app.schemas import LoginIn, RegisterIn, TokenOut, UserOut
router = APIRouter(prefix='/auth', tags=['Авторизация'])
@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == data.email)): raise HTTPException(409, 'Пользователь с таким email уже существует')
    is_admin = bool(settings.admin_email and data.email.lower() == settings.admin_email.lower())
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password), role='admin' if is_admin else 'user', is_approved=is_admin); db.add(user); db.commit(); db.refresh(user); return user
@router.post('/login', response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.password_hash): raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Неверный email или пароль')
    if not user.is_active: raise HTTPException(status.HTTP_403_FORBIDDEN, 'Пользователь заблокирован')
    if not user.is_approved: raise HTTPException(status.HTTP_403_FORBIDDEN, 'Заявка ещё не одобрена администратором')
    return TokenOut(access_token=create_access_token(user.id, user.role), user=user)
@router.get('/me', response_model=UserOut)
def me(user: User = Depends(current_user)): return user
