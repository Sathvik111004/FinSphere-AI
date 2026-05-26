import re
import os
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Union, Optional
from jose import jwt, JWTError
from app.core.config import settings

def validate_password_strength(password: str) -> None:
    """
    Validates strong passwords:
    - Minimum 12 characters (recommended)
    - Allow all character types
    """
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters long to ensure adequate security.")

def get_password_hash(password: str) -> str:
    """
    Implements industry-standard PBKDF2-SHA256 password hashing natively.
    Fully secure, high iterations, unique salts per user, and immune to passlib/bcrypt library clashes.
    """
    validate_password_strength(password)
    salt = os.urandom(16)
    # 100,000 iterations with SHA-256 matching NIST recommendations
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"pbkdf2_sha256:{salt.hex()}:{key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against the stored PBKDF2-SHA256 hash securely.
    """
    try:
        parts = hashed_password.split(":")
        if len(parts) != 3 or parts[0] != "pbkdf2_sha256":
            return False
        salt = bytes.fromhex(parts[1])
        stored_key = bytes.fromhex(parts[2])
        # Re-derive key
        derived_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100000)
        # Constant-time comparison to prevent timing attacks
        return hmac_compare_digest(derived_key, stored_key)
    except Exception:
        # Fallback comparison if hmac_compare_digest is not imported, or key length is wrong
        try:
            import hmac
            return hmac.compare_digest(derived_key, stored_key)
        except Exception:
            return False

def hmac_compare_digest(a: bytes, b: bytes) -> bool:
    import hmac
    return hmac.compare_digest(a, b)

def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # exp claim must be set and converted to integer timestamp
    to_encode = {
        "exp": int(expire.timestamp()),
        "sub": str(subject),
        "iat": int(datetime.now(timezone.utc).timestamp())
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[str]:
    """
    Harden token decoding:
    - Reject 'none' algorithm by explicitly configuring the allowed algorithm parameter.
    - Validate expiration claims explicitly.
    """
    try:
        # Hardcoding signature verification algorithm to avoid headers manipulation exploits
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM],
            options={"verify_sub": True, "verify_exp": True, "verify_iat": True}
        )
        
        # Check exp claim explicitly
        exp = payload.get("exp")
        if exp is None:
            return None
        if datetime.now(timezone.utc).timestamp() > exp:
            return None # Expired token
            
        return payload.get("sub")
    except JWTError:
        return None
