from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.core.exceptions import AuthenticationError
from app.core.security import decode_access_token
from app.database.connection import get_db
from app.database.models import User

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Dependency to resolve the current user.
    Resolves from:
    1. Authorization header (e.g., Bearer token)
    2. Secure Session Cookie
    """
    token = None
    
    # 1. Resolve from cookie (Primary for frontend matching BFF pattern guidelines)
    token = request.cookies.get("session_token")
    
    # 2. Resolve from Header (Fallback for swagger UI and scripts testing)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise AuthenticationError("Authorization session token missing.")
        
    user_id = decode_access_token(token)
    if not user_id:
        raise AuthenticationError("Session expired or token signature manipulation detected.")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AuthenticationError("Account matching this session does not exist.")
        
    return user
