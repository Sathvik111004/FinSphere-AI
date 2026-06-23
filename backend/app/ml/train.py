import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import Ridge
from app.core.config import settings

# Define target paths for serialized models
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

def build_and_train_models():
    """
    Generates synthetic datasets modeling realistic corporate balance sheets 
    and trains corporate risk, forecasting, and anomaly models.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    print("Generating synthetic corporate financial dataset...")
    
    # 1. Train Bankruptcy Prediction (Random Forest)
    # Ratios (Altman Z-Score metrics):
    # X1: Working Capital / Total Assets
    # X2: Retained Earnings / Total Assets
    # X3: EBIT / Total Assets
    # X4: Market Value Equity / Book Value Liabilities
    # X5: Sales / Total Assets
    np.random.seed(42)
    n_samples = 1000
    
    X1 = np.random.uniform(-0.2, 0.4, n_samples)
    X2 = np.random.uniform(-0.5, 0.5, n_samples)
    X3 = np.random.uniform(-0.1, 0.3, n_samples)
    X4 = np.random.uniform(0.1, 3.0, n_samples)
    X5 = np.random.uniform(0.5, 2.5, n_samples)
    
    X = np.column_stack((X1, X2, X3, X4, X5))
    
    # Bankruptcy formula based loosely on Altman Z-Score:
    # Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5
    z_score = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.99*X5
    
    # High Z-Score = safe, low Z-Score = risk
    # Probability of bankruptcy is higher if Z is small/negative
    prob = 1 / (1 + np.exp(z_score - 1.5))
    y = (prob > 0.5).astype(int)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    bankruptcy_model_path = os.path.join(MODEL_DIR, "bankruptcy_rf.joblib")
    joblib.dump(clf, bankruptcy_model_path)
    print(f"Bankruptcy model saved to {bankruptcy_model_path}")
    
    # 2. Train Revenue Forecasting (Ridge Regressor)
    # Predict future revenue based on historical quarters (1 to 4) and growth rates
    n_timeseries = 500
    quarters = []
    future_revenue = []
    
    for _ in range(n_timeseries):
        base = np.random.uniform(10.0, 500.0) # Million $
        trend = np.random.uniform(-0.05, 0.15)
        # Quarters 1, 2, 3, 4
        q1 = base * (1 + trend + np.random.normal(0, 0.02))
        q2 = q1 * (1 + trend + np.random.normal(0, 0.02))
        q3 = q2 * (1 + trend + np.random.normal(0, 0.02))
        q4 = q3 * (1 + trend + np.random.normal(0, 0.02))
        
        # Target: Quarter 5 Revenue
        q5 = q4 * (1 + trend + np.random.normal(0, 0.01))
        
        quarters.append([q1, q2, q3, q4])
        future_revenue.append(q5)
        
    X_reg = np.array(quarters)
    y_reg = np.array(future_revenue)
    
    reg = Ridge(alpha=1.0)
    reg.fit(X_reg, y_reg)
    
    forecast_model_path = os.path.join(MODEL_DIR, "revenue_ridge.joblib")
    joblib.dump(reg, forecast_model_path)
    print(f"Revenue forecasting model saved to {forecast_model_path}")
    
    # 3. Train Anomaly Detection (Isolation Forest)
    # Looks for extreme outliers in operating margin and leverage combinations
    margins = np.random.normal(0.15, 0.05, n_samples)
    leverage = np.random.normal(1.2, 0.3, n_samples)
    
    # Add manual anomalies
    margins = np.append(margins, [-0.6, 0.8, -0.4, 0.9])
    leverage = np.append(leverage, [5.5, 4.8, 6.2, 0.02])
    
    X_anomaly = np.column_stack((margins, leverage))
    
    iso = IsolationForest(contamination=0.02, random_state=42)
    iso.fit(X_anomaly)
    
    anomaly_model_path = os.path.join(MODEL_DIR, "anomaly_if.joblib")
    joblib.dump(iso, anomaly_model_path)
    print(f"Anomaly detection model saved to {anomaly_model_path}")
    print("All ML models trained and serialized successfully!")

if __name__ == "__main__":
    build_and_train_models()
