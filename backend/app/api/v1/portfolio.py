from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.services.portfolio_engine import portfolio_engine
from app.database.connection import get_db
from app.database.models import User, RecommendationHistory
from app.api.deps import get_current_user

router = APIRouter()

class PortfolioRequest(BaseModel):
    risk_profile: str = Field(..., description="Conservative, Balanced, or Aggressive")
    target_sectors: List[str] = Field(default_factory=list, description="Target allocation sectors")
    investment_objectives: str = Field("", max_length=500, description="Optional investment goals description")

class AllocationItem(BaseModel):
    asset: str
    weight: int
    color: str

class PortfolioResponse(BaseModel):
    id: str
    risk_profile: str
    allocations: List[AllocationItem]
    sector_weightings: Dict[str, float]
    explanation: str
    financial_advisory_clause: str
    created_at: str

@router.post("/generate", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def generate_portfolio(
    data: PortfolioRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Computes optimized asset allocations matching risk thresholds, 
    persisting output schemas to history.
    """
    res = portfolio_engine.generate_recommendations(
        risk_profile=data.risk_profile,
        target_sectors=data.target_sectors,
        investment_objectives=data.investment_objectives
    )
    
    # Save SQL history record
    history = RecommendationHistory(
        user_id=current_user.id,
        risk_profile=res["risk_profile"],
        sector_exposure=res["sector_weightings"],
        investment_objectives=data.investment_objectives,
        recommended_portfolio=res["allocations"],
        explanation=res["explanation"]
    )
    
    db.add(history)
    db.commit()
    db.refresh(history)
    
    return {
        "id": history.id,
        "risk_profile": res["risk_profile"],
        "allocations": res["allocations"],
        "sector_weightings": res["sector_weightings"],
        "explanation": res["explanation"],
        "financial_advisory_clause": res["financial_advisory_clause"],
        "created_at": history.created_at.isoformat()
    }

@router.get("/history", response_model=List[PortfolioResponse])
def get_portfolio_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve user-scoped asset allocations logs history.
    """
    records = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == current_user.id).order_by(RecommendationHistory.created_at.desc()).all()
    res = []
    for r in records:
        res.append({
            "id": r.id,
            "risk_profile": r.risk_profile,
            "allocations": r.recommended_portfolio,
            "sector_weightings": r.sector_exposure or {},
            "explanation": r.explanation,
            "financial_advisory_clause": "Model output based on quantitative risk indexes.",
            "created_at": r.created_at.isoformat()
        })
    return res
