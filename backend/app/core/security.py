from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pwdlib import PasswordHash
from .config import settings

ALGORITHM = 'HS256'
password_hash = PasswordHash.recommended()
def hash_password(password: str) -> str: return password_hash.hash(password)
def verify_password(password: str, password_hash_value: str) -> bool: return password_hash.verify(password, password_hash_value)
def create_access_token(user_id: int, role: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({'sub': str(user_id), 'role': role, 'exp': expires}, settings.secret_key, algorithm=ALGORITHM)
def decode_token(token: str) -> dict:
    try: return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError: return {}
