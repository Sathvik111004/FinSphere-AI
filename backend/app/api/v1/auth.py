from datetime import timedelta
from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.core.exceptions import AuthenticationError
from app.core.security import verify_password, get_password_hash, create_access_token
from app.database.connection import get_db
from app.database.models import User
from app.api.deps import get_current_user

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=12, description="Password must be at least 12 characters.")
    role: str = "analyst"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    role: str

    class Config:
        from_attributes = True

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(data: UserRegister, db: Session = Depends(get_db)):
    """
    Registers a new account. Enforces password complexity rules.
    """
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise AuthenticationError("An account with this email is already registered.")
        
    try:
        hashed = get_password_hash(data.password)
    except ValueError as e:
        raise AuthenticationError(str(e))
        
    user = User(
        email=data.email,
        hashed_password=hashed,
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    Logs in a user, returning a secure session cookie.
    """
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise AuthenticationError("Invalid email or password combination.")
        
    # Create session token
    token = create_access_token(user.id, expires_delta=timedelta(hours=2))
    
    # Set HttpOnly, Secure cookie matching secure coding requirements
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False, # Set to True in production HTTPS deployments
        samesite="lax",
        max_age=7200 # 2 hours
    )
    
    return {
        "status": "success",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/logout")
def logout(response: Response):
    """
    Invalidates session by clearing session cookies.
    """
    response.delete_cookie(
        key="session_token",
        httponly=True,
        samesite="lax"
    )
    return {"status": "success", "message": "Session logged out."}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns active user profile from secure session validation.
    """
    return current_user
