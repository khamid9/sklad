from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.database.database import get_db
from app.database.models import User
bearer = HTTPBearer()
def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    payload = decode_token(credentials.credentials); user_id = payload.get('sub')
    user = db.get(User, int(user_id)) if user_id and user_id.isdigit() else None
    if not user or not user.is_active: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Недействительный токен или пользователь заблокирован')
    return user
def admin_user(user: User = Depends(current_user)) -> User:
    if user.role != 'admin': raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Доступ только для администратора')
    return user
