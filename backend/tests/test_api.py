import unittest
import uuid
from fastapi.testclient import TestClient
from app.main import app

class TestFinSphereAPIs(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_password = "secure_audit_password_9901"

    def get_authenticated_cookies(self):
        """Helper to create a fresh user and log them in, returning authenticated cookies."""
        unique_email = f"auditor_{uuid.uuid4().hex[:8]}@finsphere.com"
        
        # 1. Signup
        reg_payload = {
            "email": unique_email,
            "password": self.test_password,
            "role": "analyst"
        }
        self.client.post("/api/v1/auth/signup", json=reg_payload)
        
        # 2. Login
        login_payload = {
            "email": unique_email,
            "password": self.test_password
        }
        login_res = self.client.post("/api/v1/auth/login", json=login_payload)
        return {"session_token": login_res.cookies.get("session_token")}

    def test_01_auth_flow(self):
        """Checks registration, login cookie emission, and logout."""
        unique_email = f"auditor_{uuid.uuid4().hex[:8]}@finsphere.com"
        
        # 1. Registration
        reg_payload = {
            "email": unique_email,
            "password": self.test_password,
            "role": "analyst"
        }
        response = self.client.post("/api/v1/auth/signup", json=reg_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], unique_email)

        # 2. Login
        login_payload = {
            "email": unique_email,
            "password": self.test_password
        }
        login_res = self.client.post("/api/v1/auth/login", json=login_payload)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn("session_token", login_res.cookies)
        
        # 3. Logout
        logout_res = self.client.post("/api/v1/auth/logout")
        self.assertEqual(logout_res.status_code, 200)

    def test_02_ml_endpoints(self):
        """Verifies ML bankruptcy scoring and timeseries forecasts."""
        cookies = self.get_authenticated_cookies()

        # Test predict risk
        risk_payload = {
            "working_capital": 45000000.0,
            "retained_earnings": 120000000.0,
            "ebit": 35000000.0,
            "equity_market_val": 280000000.0,
            "total_liabilities": 150000000.0,
            "sales": 400000000.0,
            "total_assets": 500000000.0
        }
        res = self.client.post("/api/v1/ml/predict-risk", json=risk_payload, cookies=cookies)
        self.assertEqual(res.status_code, 200)
        self.assertIn("altman_z_score", res.json())
        self.assertGreater(res.json()["altman_z_score"], 0.0)

        # Test forecast
        forecast_payload = {"quarters_history": [100.0, 110.0, 120.0, 130.0]}
        res = self.client.post("/api/v1/ml/forecast-revenue", json=forecast_payload, cookies=cookies)
        self.assertEqual(res.status_code, 200)
        self.assertIn("forecasted_revenue", res.json())

        # Test anomalies
        anomaly_payload = {"operating_margin": -0.45, "leverage_ratio": 5.2}
        res = self.client.post("/api/v1/ml/detect-anomalies", json=anomaly_payload, cookies=cookies)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["is_anomaly"])

    def test_03_portfolio_endpoints(self):
        """Verifies portfolio allocations and SQL DB storage."""
        cookies = self.get_authenticated_cookies()

        payload = {
            "risk_profile": "Balanced",
            "target_sectors": ["Technology", "Healthcare"],
            "investment_objectives": "Secure wealth preservation"
        }
        res = self.client.post("/api/v1/portfolio/generate", json=payload, cookies=cookies)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["risk_profile"], "Balanced")
        self.assertGreater(len(res.json()["allocations"]), 0)

if __name__ == "__main__":
    unittest.main()
