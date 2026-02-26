import uuid
from datetime import datetime, timedelta, timezone
from app.config import settings
from jose import JWTError, jwt

def _timestamp(dt: datetime) -> int:
    return int(dt.timestamp())

def create_access_token(uid: uuid.UUID) -> str:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub" : str(uid), # type: ignore
        "jti": str(uuid.uuid4()),
        "iat" : _timestamp(now), # type: ignore
        "exp" : _timestamp(expires), # type: ignore
        "type" : "access" # type: ignore
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
   

def create_refresh_token(uid: uuid.UUID) -> str:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub" : str(uid), # type: ignore
        "jti": str(uuid.uuid4()),
        "iat" : _timestamp(now), # type: ignore
        "exp" : _timestamp(expires), # type: ignore
        "type" : "refresh" # type: ignore
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def decode_token(token: str) -> dict | None:
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if "sub" not in payload or "jti" not in payload:
            return None

        return payload

    except JWTError:
        return None
   
