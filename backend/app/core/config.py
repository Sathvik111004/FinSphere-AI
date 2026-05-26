import os
import secrets
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

def get_fallback_jwt_secret() -> str:
    """
    Implements multi-tiered fallback for secrets matching secure coder guidelines:
    Resolution: Environment variable -> Local File Query -> Random Gen + Log
    """
    if os.getenv("JWT_SECRET_KEY"):
        return os.getenv("JWT_SECRET_KEY")
    
    secret_file = "/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/jwt_secret.txt"
    if os.path.exists(secret_file):
        try:
            with open(secret_file, "r") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Failed to read secure JWT token file: {e}")
            
    # Ephemeral secure random generation
    logger.warning("Generating ephemeral secret for session signatures. Instance-isolated!")
    token = secrets.token_hex(32)
    try:
        with open(secret_file, "w") as f:
            f.write(token)
    except Exception as e:
        logger.error(f"Failed to persist generated secret to disk: {e}")
    return token

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinSphere AI — Autonomous Financial Intelligence & Risk Decision System"
    API_V1_STR: str = "/api/v1"
    
    # Security Configurations
    JWT_SECRET: str = get_fallback_jwt_secret()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # DB Connections
    # Falls back to sqlite locally for quick demo testing if postgres is not provided
    DATABASE_URL: str = "sqlite:////Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/database.db"
    
    # RAG / AI
    CHROMA_PERSIST_DIRECTORY: str = "/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/chroma_db"
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Upload Settings
    UPLOADS_DIRECTORY: str = "/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/uploads"
    ALLOWED_EXTENSIONS: set = {"pdf", "csv", "txt"}
    MAX_FILE_SIZE_MB: int = 10
    
    model_config = SettingsConfigDict(
        env_file="/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
