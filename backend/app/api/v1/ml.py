from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Form
from pydantic import BaseModel, Field
from app.ml.prediction import ml_prediction_engine
from app.services.sentiment import sentiment_service
from app.database.models import User
from app.api.deps import get_current_user

router = APIRouter()

class RiskPredictRequest(BaseModel):
    working_capital: float = Field(..., description="Working Capital")
    retained_earnings: float = Field(..., description="Retained Earnings")
    ebit: float = Field(..., description="EBIT (Earnings Before Interest & Taxes)")
    equity_market_val: float = Field(..., description="Market Capitalization / Equity Value")
    total_liabilities: float = Field(..., description="Total Liabilities")
    sales: float = Field(..., description="Total Sales / Revenue")
    total_assets: float = Field(..., description="Total Assets")

class ForecastRequest(BaseModel):
    quarters_history: List[float] = Field(..., min_items=1, description="List of historical quarter values")

class AnomalyRequest(BaseModel):
    operating_margin: float = Field(..., description="Operating margin margin percentage (e.g. 0.15 for 15%)")
    leverage_ratio: float = Field(..., description="Debt / Assets leverage multiplier")

class TranscriptAnalysisRequest(BaseModel):
    transcript_text: str = Field(..., min_length=10, description="Raw transcription text")

@router.post("/predict-risk")
def predict_corporate_risk(data: RiskPredictRequest, current_user: User = Depends(get_current_user)):
    """
    Computes Altman Z-score and runs Random Forest classifier to output corporate bankruptcy risk indices.
    """
    return ml_prediction_engine.predict_risk_score(
        working_capital=data.working_capital,
        retained_earnings=data.retained_earnings,
        ebit=data.ebit,
        equity_market_val=data.equity_market_val,
        total_liabilities=data.total_liabilities,
        sales=data.sales,
        total_assets=data.total_assets
    )

@router.post("/forecast-revenue")
def forecast_revenue_trajectory(data: ForecastRequest, current_user: User = Depends(get_current_user)):
    """
    Runs historical Ridge regression pipelines to project next-quarter operational revenues.
    """
    return ml_prediction_engine.forecast_revenue(data.quarters_history)

@router.post("/detect-anomalies")
def scan_anomalies(data: AnomalyRequest, current_user: User = Depends(get_current_user)):
    """
    Executes Isolation Forest queries to flag structural discrepancies and accounting anomalies.
    """
    return ml_prediction_engine.detect_anomalies(
        operating_margin=data.operating_margin,
        leverage_ratio=data.leverage_ratio
    )

@router.post("/analyze-sentiment")
def analyze_transcript(data: TranscriptAnalysisRequest, current_user: User = Depends(get_current_user)):
    """
    Analyzes full-transcript executive sentiments and parses corporate risks and forward-looking guidance statements.
    """
    paragraphs = [p.strip() for p in data.transcript_text.split("\n\n") if p.strip()]
    
    # Process sentiment across paragraphs
    paragraph_sentiments = []
    overall_score = 0.0
    for p in paragraphs[:15]: # Limit to first 15 paragraphs to prevent memory overhead
        p_res = sentiment_service.analyze_paragraph_sentiment(p)
        paragraph_sentiments.append({
            "text": p[:250] + "..." if len(p) > 250 else p,
            "label": p_res["label"],
            "confidence": p_res["score"]
        })
        overall_score += p_res["raw_score"]
        
    avg_score = overall_score / len(paragraphs) if paragraphs else 0.0
    overall_label = "positive" if avg_score > 0.1 else "negative" if avg_score < -0.1 else "neutral"
    
    statements = sentiment_service.extract_key_statements(data.transcript_text)
    
    return {
        "overall_sentiment": overall_label,
        "sentiment_score": avg_score,
        "paragraph_breakdowns": paragraph_sentiments,
        "extracted_guidance": statements["guidance_statements"],
        "extracted_risks": statements["risk_statements"]
    }
