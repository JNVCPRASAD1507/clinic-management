from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from jose import JWTError, jwt
from app.core.config import settings

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        password_hasher.verify(hashed_password, password)
        return True
    except Exception:
        return False

def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
