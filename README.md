# FinSphere AI — Autonomous Financial Intelligence & Risk Decision System

FinSphere AI is an enterprise-grade financial intelligence workspace and automated risk auditing platform. Powered by a high-precision vector RAG ingestion pipeline, machine learning prediction models, and a conversational ReAct agent, it enables analysts to securely upload reports, predict revenue trends, check corporate solvency, detect accounting anomalies, and audit executive calls.

The user interface features a premium dark-mode glassmorphic theme designed to translate complex quantitative equations into clear, plain-language business insights.

---

## 🚀 Core Workspace Features

*   **📂 Ingested Reports Vault**: Upload PDF annual disclosures, CSV sheets, or TXT transcribing records. Files are automatically cleaned, converted, and indexed into secure vector search spaces.
*   **💬 AI Financial Copilot**: A conversational search copilot that references your uploaded filings. Displays a collapsible "Thinking Process" log detailing each step, from mathematical evaluation to retrieved data sources.
*   **🩺 Business Health Checker**: Computes bankruptcy risk probabilities and corporate stability tiers using historical accounting variables and Altman Z-Score coefficients.
*   **🔮 Future Revenue Predictor**: Evaluates time-series trends using Ridge regression to forecast next-quarter metrics, rendering an interactive gradient area chart.
*   **⚠️ Accounting Error Detector**: Audits margin, asset, and leverage structures using an Isolation Forest anomaly classifier to isolate reporting outliers or numerical imbalances.
*   **📊 Smart Asset Allocator**: Dynamically generates risk-adjusted portfolio weights aligned with Conservative, Balanced, or Aggressive targets.
*   **🎙️ Transcript Tone Scan**: Performs natural language sentiment parses on executive transcripts, highlighting management confidence blocks, commitments, and threat warnings.

---

## 🛠️ Technology Stack

### Backend
*   **Web Framework**: FastAPI (Python 3.11) - Asynchronous, high-throughput endpoints.
*   **Relational Storage**: SQLite (Development) / PostgreSQL (Production) using SQLAlchemy ORM.
*   **Vector Search & RAG**: ChromaDB vector index with LangChain pipelines and local Sentence-Transformers embeddings.
*   **ML & NLP Engines**: Scikit-Learn (Ridge, Isolation Forest, Random Forest) & custom TF-IDF Call sentiment metrics.

### Frontend
*   **Framework**: Next.js 14 (App Router) & React 18.
*   **Styles & Graphics**: Tailwind CSS & PostCSS (glowing radial accents, glassmorphic panel filters).
*   **Interactive Visuals**: Recharts (smooth gradient linear area graphs, dynamic allocation donut rings).
*   **Icons**: Lucide Icons.

---

## ⚙️ Configuration & Environment Setup

The system works out-of-the-box in local fallback sandbox mode. To enable dynamic AI-powered audits and real-time reasoning, create a `.env` file inside the root folder using `.env.example` as a blueprint:

```env
# Relational Database connection
DATABASE_URL="sqlite:////Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/database.db"

# Vector Database local persistence path
CHROMA_PERSIST_DIRECTORY="/Users/sathvikgattu/.gemini/antigravity-ide/scratch/finsphere-ai/chroma_db"

# Reasoning API Keys (Configure one of the following for real-time AI)
OPENAI_API_KEY="your-openai-api-key-here"
GEMINI_API_KEY="your-gemini-api-key-here"
```

---

## 💻 Local Development Startup

### 1. Boot up the Backend Server
```bash
# Navigate to backend directory
cd backend

# Install python dependencies
pip install -r requirements.txt

# Run the Uvicorn application server
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
*API Endpoint Doc pages will be available at:* `http://127.0.0.1:8000/docs`

### 2. Boot up the Frontend UI Client
```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Clear Next.js cache and start development server
rm -rf .next
npm run dev
```
*Open and view the application dashboard at:* `http://localhost:3000`

---

## 🧪 Enterprise Verification & Diagnostics

To run the offline system diagnostics and check the integrity of all database routes, ML classifiers, and RAG pipelines:

```bash
cd backend
python3 run_diagnostics.py
```
*A successful sweep will output:* `FinSphere AI Platform — Enterprise Diagnostics successfully completed!`
