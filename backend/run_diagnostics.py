#!/usr/bin/env python3
import os
import sys
import uuid
import logging
from fastapi.testclient import TestClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("FinSphereDiagnostics")

# Add the backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

def run_diagnostics():
    logger.info("================================================================================")
    logger.info("FinSphere AI Platform — End-to-End Enterprise Diagnostic Test Runner")
    logger.info("================================================================================")

    # Initialize the TestClient
    client = TestClient(app)
    logger.info("1. Initialized FastAPI TestClient successfully.")

    # -------------------------------------------------------------------------
    # PART 1: User Security Authentication Flows
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 1] Security & Authentication ---")
    unique_id = uuid.uuid4().hex[:8]
    test_email = f"diagnostics_auditor_{unique_id}@finsphere.com"
    test_password = "secure_audit_password_9901"
    
    # Sign up
    signup_payload = {
        "email": test_email,
        "password": test_password,
        "role": "analyst"
    }
    signup_res = client.post("/api/v1/auth/signup", json=signup_payload)
    if signup_res.status_code == 201:
        logger.info(f"✔ Auth Signup: SUCCESS. Account created for {test_email}")
    else:
        logger.error(f"❌ Auth Signup: FAILED ({signup_res.status_code}): {signup_res.text}")
        return

    # Login
    login_payload = {
        "email": test_email,
        "password": test_password
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    if login_res.status_code == 200:
        logger.info("✔ Auth Login: SUCCESS. Session token emitted in cookie.")
    else:
        logger.error(f"❌ Auth Login: FAILED ({login_res.status_code}): {login_res.text}")
        return

    session_token = login_res.cookies.get("session_token")
    cookies = {"session_token": session_token}

    # Fetch User Info
    me_res = client.get("/api/v1/auth/me", cookies=cookies)
    if me_res.status_code == 200:
        logger.info(f"✔ Auth Me Hook: SUCCESS. Authenticated as: {me_res.json().get('email')}")
    else:
        logger.error(f"❌ Auth Me Hook: FAILED: {me_res.text}")

    # -------------------------------------------------------------------------
    # PART 2: Document Ingestion and Magic Header Parsing
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 2] Document Ingestion Engine ---")
    test_docs_path = "/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/test_documents"
    
    ingested_docs = []
    
    for filename, doc_type in [
        ("annual_report_sample.txt", "annual_report"),
        ("earnings_transcript_sample.txt", "transcript"),
        ("portfolio_raw_data.csv", "SEC_filing")
    ]:
        full_path = os.path.join(test_docs_path, filename)
        if not os.path.exists(full_path):
            logger.error(f"❌ File not found: {full_path}. Create documents first.")
            continue
            
        with open(full_path, "rb") as f:
            files = {"file": (filename, f, "text/plain")}
            data = {"document_type": doc_type}
            
            upload_res = client.post(
                "/api/v1/documents/upload",
                files=files,
                data=data,
                cookies=cookies
            )
            
            if upload_res.status_code == 201:
                uploaded_meta = upload_res.json()
                logger.info(f"✔ Document Upload: SUCCESS [{filename}]. Ingestion ID: {uploaded_meta['id']}")
                ingested_docs.append(uploaded_meta)
            else:
                logger.error(f"❌ Document Upload FAILED for {filename} ({upload_res.status_code}): {upload_res.text}")

    # List documents
    list_res = client.get("/api/v1/documents/", cookies=cookies)
    if list_res.status_code == 200:
        logger.info(f"✔ Document List Hook: SUCCESS. Total indexed user documents: {len(list_res.json())}")
    else:
        logger.error(f"❌ Document List Hook: FAILED: {list_res.text}")

    # -------------------------------------------------------------------------
    # PART 3: Vector RAG Grounding Search
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 3] Vector Grounded RAG Search ---")
    rag_payload = {
        "query": "What is the expected operating margin outlook in 2026?"
    }
    rag_res = client.post("/api/v1/rag/query", json=rag_payload, cookies=cookies)
    if rag_res.status_code == 200:
        res_data = rag_res.json()
        logger.info("✔ RAG Pipeline: SUCCESS.")
        logger.info(f"  - Retrieved Chunks Count: {res_data.get('retrieved_chunks_count')}")
        logger.info(f"  - Answer Snippet: {res_data.get('answer')[:120]}...")
    else:
        logger.error(f"❌ RAG Pipeline: FAILED: {rag_res.text}")

    # -------------------------------------------------------------------------
    # PART 4: Machine Learning Risk Decision & NLP Sentiment Engines
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 4] Machine Learning Risk, Forecasting & Sentiment Engines ---")
    
    # 4a. Predict risk
    risk_payload = {
        "working_capital": 45000000.0,
        "retained_earnings": 120000000.0,
        "ebit": 35000000.0,
        "equity_market_val": 280000000.0,
        "total_liabilities": 150000000.0,
        "sales": 400000000.0,
        "total_assets": 500000000.0
    }
    risk_res = client.post("/api/v1/ml/predict-risk", json=risk_payload, cookies=cookies)
    if risk_res.status_code == 200:
        logger.info("✔ ML Altman Z-Score Risk: SUCCESS.")
        logger.info(f"  - Altman Z-Score: {risk_res.json().get('altman_z_score')}")
        logger.info(f"  - Risk Assessment Class: {risk_res.json().get('risk_class')}")
    else:
        logger.error(f"❌ ML Altman Z-Score: FAILED: {risk_res.text}")

    # 4b. Forecast Revenue
    forecast_payload = {
        "quarters_history": [100.0, 110.0, 120.0, 130.0]
    }
    forecast_res = client.post("/api/v1/ml/forecast-revenue", json=forecast_payload, cookies=cookies)
    if forecast_res.status_code == 200:
        logger.info("✔ ML Ridge Revenue Forecasting: SUCCESS.")
        logger.info(f"  - Next Quarter Projection: {forecast_res.json().get('forecasted_revenue')}M")
    else:
        logger.error(f"❌ ML Ridge Revenue Forecasting: FAILED: {forecast_res.text}")

    # 4c. Detect Anomalies
    anomaly_payload = {
        "operating_margin": -0.45,
        "leverage_ratio": 5.2
    }
    anomaly_res = client.post("/api/v1/ml/detect-anomalies", json=anomaly_payload, cookies=cookies)
    if anomaly_res.status_code == 200:
        logger.info("✔ ML Isolation Forest Anomaly Detection: SUCCESS.")
        logger.info(f"  - Is Anomaly: {anomaly_res.json().get('is_anomaly')}")
        logger.info(f"  - Outlier Score: {anomaly_res.json().get('outlier_score')}")
    else:
        logger.error(f"❌ ML Isolation Forest Anomaly Detection: FAILED: {anomaly_res.text}")

    # 4d. Sentiment Analysis
    transcript_text = (
        "We delivered robust revenue growth of 18% year-over-year, beat our expectations. "
        "Our enterprise cloud platforms outperformed expectations, driven by strong growth in SaaS adoptions. "
        "Consequently, our operating margin improved to 22%, representing solid profitability expansion.\n\n"
        "However, we expect persistent macroeconomic headwinds to create challenges in our EMEA channels. "
        "We see a moderate contraction and deficit in supply chain logistics margins, representing liquidity-concerns. "
        "We also face a potential lawsuit from proprietary infringements, which could cause a shortfall.\n\n"
        "Looking forward to the future, our target guidance outlines a positive revenue outlook. "
        "We target capital capex expansions of $45M as we expect robust synergies."
    )
    sentiment_payload = {
        "transcript_text": transcript_text
    }
    sentiment_res = client.post("/api/v1/ml/analyze-sentiment", json=sentiment_payload, cookies=cookies)
    if sentiment_res.status_code == 200:
        logger.info("✔ NLP Call Sentiment Analysis: SUCCESS.")
        logger.info(f"  - Overall Call Sentiment: {sentiment_res.json().get('overall_sentiment')}")
        logger.info(f"  - Average Sentiment Index: {sentiment_res.json().get('sentiment_score')}")
        logger.info(f"  - Extracted Guidance count: {len(sentiment_res.json().get('extracted_guidance'))}")
        logger.info(f"  - Extracted Risks count: {len(sentiment_res.json().get('extracted_risks'))}")
    else:
        logger.error(f"❌ NLP Call Sentiment Analysis: FAILED: {sentiment_res.text}")

    # -------------------------------------------------------------------------
    # PART 5: AI Portfolio Allocation & Optimization Engine
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 5] AI Portfolio Allocation & Optimization ---")
    portfolio_payload = {
        "risk_profile": "Balanced",
        "target_sectors": ["Technology", "Healthcare", "Energy"],
        "investment_objectives": "Generate sustainable yield with balanced capital preservation targets"
    }
    portfolio_res = client.post("/api/v1/portfolio/generate", json=portfolio_payload, cookies=cookies)
    if portfolio_res.status_code == 201:
        logger.info("✔ Portfolio Generation: SUCCESS.")
        logger.info(f"  - Selected Profile: {portfolio_res.json().get('risk_profile')}")
        logger.info(f"  - Allocated Assets: {portfolio_res.json().get('allocations')}")
    else:
        logger.error(f"❌ Portfolio Generation: FAILED: {portfolio_res.text}")

    # -------------------------------------------------------------------------
    # PART 6: ReAct Autonomous Agent Executor
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 6] ReAct Autonomous Financial Analyst Agent ---")
    agent_payload = {
        "prompt": "Analyze my sample data and calculate the Altman Z solvency score and check for anomalies."
    }
    agent_res = client.post("/api/v1/analyst/run-task", json=agent_payload, cookies=cookies)
    if agent_res.status_code == 200:
        logger.info("✔ ReAct Analyst Agent Execution: SUCCESS.")
        logger.info(f"  - Agent Recommendations Report Snippet:\n{agent_res.json().get('output')[:300]}...")
    else:
        logger.error(f"❌ ReAct Analyst Agent: FAILED: {agent_res.text}")

    # -------------------------------------------------------------------------
    # PART 7: Document Indices Tear Down (Cleaning upload state)
    # -------------------------------------------------------------------------
    logger.info("\n--- [PART 7] Vector Index & Document Tear Down ---")
    for doc in ingested_docs:
        del_res = client.delete(f"/api/v1/documents/{doc['id']}", cookies=cookies)
        if del_res.status_code == 200:
            logger.info(f"✔ Document Tear Down: SUCCESS. Cleaned up ID: {doc['id']}")
        else:
            logger.error(f"❌ Document Tear Down: FAILED for ID: {doc['id']}: {del_res.text}")

    # -------------------------------------------------------------------------
    # Diagnostic Complete summary
    # -------------------------------------------------------------------------
    logger.info("\n================================================================================")
    logger.info("FinSphere AI Platform — Enterprise Diagnostics successfully completed!")
    logger.info("================================================================================")

if __name__ == "__main__":
    run_diagnostics()
