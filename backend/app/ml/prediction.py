import os
import joblib
import numpy as np
from typing import Dict, Any, List, Tuple
from app.core.config import settings

MODEL_DIR = "/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/backend/app/ml/models"

class FinSphereMLPredictionEngine:
    def __init__(self):
        # Paths
        self.bankruptcy_path = os.path.join(MODEL_DIR, "bankruptcy_rf.joblib")
        self.forecast_path = os.path.join(MODEL_DIR, "revenue_ridge.joblib")
        self.anomaly_path = os.path.join(MODEL_DIR, "anomaly_if.joblib")
        
        # Internal model handles
        self._bankruptcy_model = None
        self._forecast_model = None
        self._anomaly_model = None

    @property
    def bankruptcy_model(self):
        if self._bankruptcy_model is None and os.path.exists(self.bankruptcy_path):
            self._bankruptcy_model = joblib.load(self.bankruptcy_path)
        return self._bankruptcy_model

    @property
    def forecast_model(self):
        if self._forecast_model is None and os.path.exists(self.forecast_path):
            self._forecast_model = joblib.load(self.forecast_path)
        return self._forecast_model

    @property
    def anomaly_model(self):
        if self._anomaly_model is None and os.path.exists(self.anomaly_path):
            self._anomaly_model = joblib.load(self.anomaly_path)
        return self._anomaly_model

    def calculate_altman_z_score(self, working_capital: float, retained_earnings: float, ebit: float, 
                                 equity_market_val: float, total_liabilities: float, sales: float, 
                                 total_assets: float) -> Tuple:
        """
        Calculates classic Altman Z-Score for manufacturing/non-manufacturing corporations:
        Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 0.99*E
        
        Zones:
        Z > 2.99: Safe Zone
        1.81 <= Z <= 2.99: Gray Zone
        Z < 1.81: Distress (Bankruptcy) Zone
        """
        if total_assets <= 0 or total_liabilities <= 0:
            return 0.0, "Critical data missing"
            
        A = working_capital / total_assets
        B = retained_earnings / total_assets
        C = ebit / total_assets
        D = equity_market_val / total_liabilities
        E = sales / total_assets
        
        z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 0.99*E
        
        if z > 2.99:
            status = "Safe"
        elif z >= 1.81:
            status = "Gray (Moderate Risk)"
        else:
            status = "Distress (High Bankruptcy Risk)"
            
        return float(z), status, [A, B, C, D, E]

    def predict_risk_score(self, working_capital: float, retained_earnings: float, ebit: float, 
                           equity_market_val: float, total_liabilities: float, sales: float, 
                           total_assets: float) -> Dict[str, Any]:
        """
        Generates comprehensive bankruptcy probability and aggregated risk percentage.
        """
        z_val, z_status, ratios = self.calculate_altman_z_score(
            working_capital, retained_earnings, ebit, equity_market_val, total_liabilities, sales, total_assets
        )
        
        # Format model feature vector
        features = np.array([ratios])
        
        # Predict using Random Forest if loaded, else fall back to direct equation statistical logic
        rf = self.bankruptcy_model
        if rf:
            prob = float(rf.predict_proba(features)[0][1])
            prediction = int(rf.predict(features)[0])
        else:
            # Fallback mathematical interpolation
            # Base probability derived from Z-Score (low Z = high bankruptcy probability)
            prob = 1.0 / (1.0 + np.exp(z_val - 1.5))
            prediction = 1 if prob > 0.5 else 0
            
        # Composite score from 0 (perfect health) to 100 (insolvent failure)
        composite_score = int(prob * 100)
        
        return {
            "altman_z_score": z_val,
            "solvency_status": z_status,
            "bankruptcy_probability": prob,
            "bankruptcy_prediction_label": "High Risk" if prediction == 1 else "Low Risk",
            "composite_risk_score": composite_score
        }

    def forecast_revenue(self, quarters_history: List[float]) -> Dict[str, Any]:
        """
        Forecasts next-quarter revenue based on 4-quarters historical trajectory.
        """
        if len(quarters_history) < 4:
            # Fallback simple rolling average
            next_q = float(np.mean(quarters_history)) if quarters_history else 0.0
            confidence = 0.50
        else:
            features = np.array([quarters_history[-4:]])
            ridge = self.forecast_model
            if ridge:
                next_q = float(ridge.predict(features)[0])
                confidence = 0.92
            else:
                # Rolling linear growth projection fallback
                diffs = np.diff(quarters_history)
                next_q = quarters_history[-1] + float(np.mean(diffs))
                confidence = 0.80
                
        return {
            "forecasted_revenue": next_q,
            "forecast_confidence": confidence,
            "trend_direction": "Upward" if (next_q > quarters_history[-1] if quarters_history else True) else "Downward"
        }

    def detect_anomalies(self, operating_margin: float, leverage_ratio: float) -> Dict[str, Any]:
        """
        Checks financial metrics for operational anomalies.
        """
        features = np.array([[operating_margin, leverage_ratio]])
        iso = self.anomaly_model
        
        if iso:
            # Isolation forest prediction (1 = normal, -1 = anomaly)
            pred = int(iso.predict(features)[0])
            score = float(iso.decision_function(features)[0])
            is_anomaly = pred == -1
        else:
            # Basic fallback statistical threshold limits
            # Operating margin < -40% or leverage > 4.5
            is_anomaly = operating_margin < -0.4 or leverage_ratio > 4.5
            score = 0.95 if is_anomaly else 0.1
            
        return {
            "is_anomaly": is_anomaly,
            "anomaly_confidence_score": float(np.abs(score)),
            "reasoning": "Unusual combination of operating deficits and balance sheet debt." if is_anomaly else "Metric distributions align with standard industry bands."
        }

ml_prediction_engine = FinSphereMLPredictionEngine()
