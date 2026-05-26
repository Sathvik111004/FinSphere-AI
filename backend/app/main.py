import logging
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.database.connection import engine, Base
from app.api.v1 import auth, documents, rag, ml, agents, portfolio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Automate SQLite / DB Tables initialization matching development specs
try:
    Base.metadata.create_all(bind=engine)
    logger.info("SQL database structural schema synchronized successfully.")
except Exception as e:
    logger.critical(f"Failed to synchronize relational database boundaries: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise-Grade AI-Powered Financial Intelligence & Risk Decision Platform APIs.",
    version="1.0.0"
)

# Apply CORS boundaries. RESTRICT to specific trusted origins (no wildcards '*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Cookie"],
    expose_headers=["Set-Cookie"]
)

# Global Security Headers Interceptor Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
    return response

# Handle and mask SQLAlchemy database-level warnings
@app.exception_handler(SQLAlchemyError)
def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Internal SQL Execution Warning: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Relational query execution error. Diagnostic hashes logged securely."}
    )

# Wire core routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(rag.router, prefix=f"{settings.API_V1_STR}/rag", tags=["rag"])
app.include_router(ml.router, prefix=f"{settings.API_V1_STR}/ml", tags=["ml"])
app.include_router(agents.router, prefix=f"{settings.API_V1_STR}/analyst", tags=["analyst"])
app.include_router(portfolio.router, prefix=f"{settings.API_V1_STR}/portfolio", tags=["portfolio"])

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "mode": "Sandbox Developer Local"
    }
