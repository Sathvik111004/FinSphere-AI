import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.connection import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="analyst")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    documents = relationship("DocumentMetadata", back_populates="owner", cascade="all, delete-orphan")
    recommendations = relationship("RecommendationHistory", back_populates="owner", cascade="all, delete-orphan")

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    document_type = Column(String(50), nullable=False) # e.g. annual_report, transcript
    size_bytes = Column(Integer, nullable=False)
    ingestion_status = Column(String(50), default="pending") # pending, success, failed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    owner = relationship("User", back_populates="documents")

class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    risk_profile = Column(String(50), nullable=False) # e.g. low, medium, high
    sector_exposure = Column(JSON, nullable=True) # Selected target sectors list
    investment_objectives = Column(String(500), nullable=True)
    recommended_portfolio = Column(JSON, nullable=False) # Visual weights mapping
    explanation = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    owner = relationship("User", back_populates="recommendations")
