from langchain.tools import tool
from typing import Dict, Any, List
from app.rag.pipeline import rag_pipeline
from app.ml.prediction import ml_prediction_engine

@tool
def financial_vector_search(query: str, user_id: str) -> str:
    """
    Queries the FinSphere vector database to retrieve grounded context, citations, 
    and quantitative insights from uploaded financial documents. Use this whenever 
    you need numbers, balances, transcripts, or audit summaries.
    """
    res = rag_pipeline.query_financial_knowledge(query, user_id)
    return f"Retrieved Answer:\n{res['answer']}\nSources: {', '.join(res['sources'])}"

@tool
def ratio_calculator(working_capital: float, retained_earnings: float, ebit: float, 
                     equity_market_val: float, total_liabilities: float, sales: float, 
                     total_assets: float) -> str:
    """
    Computes classic Altman Z-Score and key financial ratios. 
    Accepts raw balance sheet variables and returns risk scoring evaluations.
    """
    res = ml_prediction_engine.predict_risk_score(
        working_capital, retained_earnings, ebit, equity_market_val, total_liabilities, sales, total_assets
    )
    return (
        f"Altman Z-Score: {res['altman_z_score']:.2f}\n"
        f"Solvency Zone: {res['solvency_status']}\n"
        f"Statistical Bankruptcy Probability: {res['bankruptcy_probability']*100:.1f}%\n"
        f"Composite Risk Metric: {res['composite_risk_score']}/100"
    )

@tool
def revenue_forecaster(quarters_history: List[float]) -> str:
    """
    Runs regression models to predict next-quarter revenue based on 
    historical performance numbers. Accepts historical float lists.
    """
    res = ml_prediction_engine.forecast_revenue(quarters_history)
    return (
        f"Forecasted Revenue: ${res['forecasted_revenue']:.2f}M\n"
        f"Trend Vector: {res['trend_direction']}\n"
        f"Statistical Confidence: {res['forecast_confidence']*100:.1f}%"
    )

@tool
def anomaly_detector(operating_margin: float, leverage_ratio: float) -> str:
    """
    Analyzes operating margin and leverage metrics to flag unusual 
    outliers or bookkeeping warning flags.
    """
    res = ml_prediction_engine.detect_anomalies(operating_margin, leverage_ratio)
    status = "ANOMALOUS ACTIVITY DETECTED" if res["is_anomaly"] else "Normal balance"
    return f"Anomaly Check: {status}\nExplanation: {res['reasoning']}\nConfidence: {res['anomaly_confidence_score']*100:.1f}%"
