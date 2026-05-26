# FinSphere-AI
FinSphere AI is an enterprise-grade financial intelligence workspace and automated risk auditing platform. Powered by a high-precision vector RAG ingestion pipeline, natural language processing (NLP), and statistical machine learning models, it empowers business analysts to securely upload reports, forecast revenues, evaluate bankruptcy/solvency zones, and chat with an autonomous financial copilot.

The platform is designed with a premium glassmorphic dark-mode dashboard interface, translating complex quantitative equations into friendly, plain-language business insights.

🚀 Core Features
📂 Data Ingestion & Vault: Drag-and-drop support for PDF annual reports (10-K), CSV datasets, and text transcripts. Files are automatically vectorized into a secure database.
💬 AI Financial Copilot: A context-aware conversational auditor capable of retrieving corporate filings and answering quantitative questions, complete with a collapsible "Thinking Process" log detailing its calculations.
📈 Business Health & Solvency Estimator: Evaluates balance sheet variables using machine learning and solvency ratios (Altman Z-Score) to forecast corporate stability and bankruptcy probabilities.
🔮 Future Revenue Predictor: Fits regularized regression models (Ridge) to historical quarterly data to project upcoming growth trajectories, rendered in an interactive gradient Area chart.
🔍 Accounting Error Detector: Scans margin and leverage records using anomaly-detection models (Isolation Forest) to isolate reporting outliers or accounting discrepancies.
📊 Smart Investment Allocator: Custom-diversifies portfolio distributions based on user risk profiles (Conservative, Balanced, Aggressive) and target market industries.
🎙️ Call Tone & Sentiment Scan: Parses earnings call transcripts paragraph-by-paragraph to highlight executive confidence metrics, extracted commitments, and threat warnings.
🛠️ Technology Stack
Backend (Core Engine)
Framework: FastAPI (Python 3.11) — high-speed asynchronous REST endpoints.
Database & ORM: PostgreSQL (Production) / SQLite (Local) with SQLAlchemy.
Vector Search & RAG: ChromaDB vector store paired with LangChain and offline Sentence-Transformers embeddings.
Machine Learning & NLP: Scikit-Learn (Ridge, Isolation Forest, Random Forest) & custom TF-IDF sentiment models.
Frontend (UI Client)
Framework: Next.js 14 (App Router) & React 18.
Styling & Effects: Tailwind CSS, PostCSS, and Custom HSL Glassmorphism filters.
Data Visualization: Recharts (smooth gradient linear area charts, donut allocation rings).
Icons & Assets: Lucide React.
⚙️ Quick Start
Prerequisites
Python 3.11+
Node.js 18+
1. Run the FastAPI Backend
bash
cd backend
# Install dependencies
pip install -r requirements.txt
# Run server (bound to localhost:8000)
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
2. Run the Next.js Frontend
bash
cd frontend
# Install dependencies
npm install
# Clear Next.js cache and start development server
rm -rf .next
npm run dev
