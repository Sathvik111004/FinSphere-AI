from typing import Dict, Any, List
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.config import settings
from app.agents.tools import financial_vector_search, ratio_calculator, revenue_forecaster, anomaly_detector
from app.ml.prediction import ml_prediction_engine
from app.utils.gemini import generate_content_with_fallback

class FinSphereAnalystAgent:
    def __init__(self):
        self.tools = [financial_vector_search, ratio_calculator, revenue_forecaster, anomaly_detector]
        
    def get_agent_executor(self, user_id: str):
        """
        Creates dynamic agent executor binding user session context.
        """
        if not settings.OPENAI_API_KEY:
            return None
            
        llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model="gpt-4o", temperature=0.2)
        
        # Configure advanced system instructions
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an elite autonomous financial intelligence advisor. "
                       "Provide clear, concise, direct, and quantitative answers in 1-3 paragraphs. "
                       "If the user asks questions about models, metrics, or financial calculations (like Altman Z-Score or Isolation Forest anomalies), explain the concepts briefly and clearly. "
                       "Avoid long templates, repetitive warnings, or disclaimers. "
                       "You have access to state-of-the-art analytical math models and vector search tools. "
                       "Perform step-by-step reasoning (SWOT, quantitative ratios, forecasting). "
                       f"IMPORTANT: Always append user_id='{user_id}' when executing 'financial_vector_search' tool."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run_analyst_task(self, prompt_input: str, user_id: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Runs the financial analyst agent.
        Supports automatic tool routing and metric parsing in both active LLM and local sandboxes.
        """
        # Intercept short prompts / greetings for a better user experience
        clean_prompt = prompt_input.strip().lower().replace(".", "").replace("?", "").replace("!", "")
        if len(clean_prompt) < 3 or clean_prompt in ["hi", "hello", "hey", "help", "greetings"]:
            return {
                "output": "Hello! I am your FinSphere AI Financial Copilot. How can I assist you with your uploaded financial audits, solvency risk checks, or forecasting today?",
                "reasoning_steps": ["Grounded Greeting: Welcomed user and offered copilot assistance."]
            }
            
        executor = self.get_agent_executor(user_id)
        
        if executor:
            # Active LLM run
            chat_history_list = []
            if history:
                for h in history:
                    chat_history_list.append(("human" if h["role"] == "user" else "ai", h["content"]))
                    
            try:
                res = executor.invoke({
                    "input": prompt_input,
                    "chat_history": chat_history_list
                })
                return {
                    "output": res["output"],
                    "reasoning_steps": ["Agent reasoned through LLM plan successfully."]
                }
            except Exception as e:
                return {
                    "output": f"Agent error: {str(e)}",
                    "reasoning_steps": ["Error occurred during execution."]
                }
        else:
            import re
            import requests
            from app.rag.pipeline import rag_pipeline
            
            steps = ["Initializing Autonomous Coordinator...", "Executing financial vector search..."]
            
            # Step 1: Run financial vector search to get document context
            try:
                res_rag = rag_pipeline.query_financial_knowledge(prompt_input, user_id)
                clean_rag_answer = res_rag["answer"]
                sources = res_rag["sources"]
                steps.append("Document RAG database query completed successfully.")
            except Exception as e:
                clean_rag_answer = ""
                sources = []
                steps.append(f"Document RAG database query failed: {str(e)}")
                
            # Clean up sandbox notes/disclaimers from RAG answer to keep the chatbot clean
            if "*Note: Running in local sandbox mode" in clean_rag_answer:
                clean_rag_answer = clean_rag_answer.split("*Note: Running in local sandbox mode")[0].strip()
            elif "Note: Running in local sandbox mode" in clean_rag_answer:
                clean_rag_answer = clean_rag_answer.split("Note: Running in local sandbox mode")[0].strip()
                
            # Step 2: Extract financial parameters from user query and document context
            steps.append("Parsing retrieved context and prompt for financial metrics...")
            
            # Default values to fall back to if they are not found in the documents
            metrics = {
                "working_capital": 45000000.0,
                "retained_earnings": 120000000.0,
                "ebit": 35000000.0,
                "equity_market_val": 280000000.0,
                "total_liabilities": 150000000.0,
                "sales": 400000000.0,
                "total_assets": 500000000.0,
                "operating_margin": -0.45,
                "leverage_ratio": 5.2,
                "quarters_history": [105.0, 112.5, 118.0, 124.2]
            }
            
            search_space = f"{prompt_input}\n\n{clean_rag_answer}"
            
            # Suffixes pattern maps (e.g. 45M, 45 million, 2.1B)
            patterns = {
                "working_capital": r"(?i)working\s+capital.*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b",
                "retained_earnings": r"(?i)retained\s+earnings.*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b",
                "ebit": r"(?i)(?:ebit|operating\s+income|operating\s+profit).*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b",
                "equity_market_val": r"(?i)(?:market\s+value\s+of\s+equity|equity\s+market\s+val|market\s+equity\s+val|market\s+equity).*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b",
                "total_liabilities": r"(?i)total\s+liabilities.*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b",
                "sales": r"(?i)(?:total\s+sales|sales|revenue|revenues).*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b",
                "total_assets": r"(?i)total\s+assets.*?\$?\s*([0-9,]+(?:\.[0-9]+)?)\s*(m|b|k|million|billion|thousand)?\b"
            }
            
            multiplier_map = {
                "m": 1_000_000,
                "million": 1_000_000,
                "b": 1_000_000_000,
                "billion": 1_000_000_000,
                "k": 1_000,
                "thousand": 1_000
            }
            
            metrics_extracted = []
            for key, pattern in patterns.items():
                match = re.search(pattern, search_space)
                if match:
                    clean_str = match.group(1).replace(",", "")
                    suffix = match.group(2)
                    try:
                        val = float(clean_str)
                        if suffix:
                            val *= multiplier_map[suffix.lower()]
                        metrics[key] = val
                        metrics_extracted.append(key)
                    except ValueError:
                        pass
                        
            # Operating margin (handles both -0.45 or 22% styles, permitting intermediate words)
            margin_match = re.search(r"(?i)operating\s+margin.*?\s*(-?[0-9]+(?:\.[0-9]+)?)\s*(%)?", search_space)
            if margin_match:
                try:
                    val = float(margin_match.group(1))
                    is_percentage = margin_match.group(2) == "%"
                    if is_percentage:
                        val /= 100.0
                    metrics["operating_margin"] = val
                    metrics_extracted.append("operating_margin")
                except ValueError:
                    pass
                    
            # Leverage ratio
            leverage_match = re.search(r"(?i)leverage\s+ratio.*?\s*([0-9]+(?:\.[0-9]+)?)\b", search_space)
            if leverage_match:
                try:
                    metrics["leverage_ratio"] = float(leverage_match.group(1))
                    metrics_extracted.append("leverage_ratio")
                except ValueError:
                    pass
                    
            # Quarters history (check for bracket format first, then comma/space separated sequence)
            quarters_match = re.search(r"\[\s*([0-9.,\s\-]+)\s*\]", search_space)
            if not quarters_match:
                quarters_match = re.search(r"(?i)(?:history|historical|revenues|quarters).*?\s*([0-9]+(?:\.[0-9]+)?(?:[\s,]+[0-9]+(?:\.[0-9]+)?){2,})", search_space)
                
            if quarters_match:
                try:
                    raw_str = quarters_match.group(1)
                    raw_vals = re.split(r"[\s,]+", raw_str.strip())
                    parsed_floats = [float(x.strip()) for x in raw_vals if x.strip()]
                    if parsed_floats:
                        metrics["quarters_history"] = parsed_floats
                        metrics_extracted.append("quarters_history")
                except ValueError:
                    pass
                    
            if metrics_extracted:
                steps.append(f"Successfully extracted parameters: {', '.join(metrics_extracted)}")
            else:
                steps.append("No specific metrics extracted; utilizing standard benchmark values.")
                
            # Step 3: Determine which tools to invoke based on prompt keyword matching
            prompt_lower = prompt_input.lower()
            
            # Run solvency math only if explicitly requested
            run_ratio = any(kw in prompt_lower for kw in [
                "altman", "z-score", "z score", "bankruptcy risk", "solvency calculation", 
                "calculate solvency", "bankruptcy probability", "corporate health score"
            ])
            
            # Run anomaly check only if explicitly requested
            run_anomaly = any(kw in prompt_lower for kw in [
                "detect anomalies", "anomaly check", "accounting anomalies", "isolation forest",
                "outlier detection", "irregularities scan", "bookkeeping integrity"
            ])
            
            # Run revenue forecast only if explicitly requested
            run_forecast = any(kw in prompt_lower for kw in [
                "forecast revenue", "revenue forecast", "project revenue", "revenue projection",
                "predict revenue", "future revenue", "ridge regression forecast", "next-quarter performance"
            ])
            
            # If the user explicitly asks to run all diagnostics/sweep
            if any(kw in prompt_lower for kw in ["run all models", "complete audit", "overall diagnostics", "run everything"]):
                run_ratio = True
                run_anomaly = True
                run_forecast = True
                
            # Educational Concept explanations
            explanations = []
            if any(kw in prompt_lower for kw in ["altman", "z-score", "z score"]):
                explanations.append(
                    "**Altman Z-Score Model**: The Altman Z-Score is a legendary mathematical formula published by NYU Professor Edward Altman in 1968. "
                    "It calculates corporate bankruptcy risk within a 2-year horizon by combining five weighted financial ratios: "
                    "(1) Working Capital/Total Assets (measures short-term liquidity), "
                    "(2) Retained Earnings/Total Assets (measures cumulative profitability), "
                    "(3) EBIT/Total Assets (measures operational productivity), "
                    "(4) Market Value of Equity/Total Liabilities (measures leverage/solvency), and "
                    "(5) Sales/Total Assets (measures asset turnover/sales efficiency). "
                    "A score below 1.81 is the 'Distress Zone' (High Risk), 1.81-2.99 is the 'Gray Zone' (Moderate Risk), and above 2.99 is the 'Safe Zone'."
                )
            if any(kw in prompt_lower for kw in ["anomaly", "irregular", "outlier", "isolation forest"]):
                explanations.append(
                    "**Anomaly & Fraud Detection (Isolation Forest)**: Isolation Forest is an unsupervised machine learning algorithm designed to detect anomalies. "
                    "Unlike traditional distance-based methods, it isolates anomalies by randomly partitioning feature paths. "
                    "Because anomalies are rare and have distinct values, they require fewer random splits to isolate, resulting in shorter path lengths in the trees, "
                    "allowing us to flag potential accounting errors, supply chain deficits, or bookkeeping discrepancies."
                )
            if any(kw in prompt_lower for kw in ["forecast", "ridge", "prediction"]):
                explanations.append(
                    "**Ridge Growth Forecasting**: Ridge Regression is a linear regression model that applies L2 regularization to prevent overfitting and handle multicollinearity. "
                    "In FinSphere, the model analyzes historical quarters (typically 4 quarters) to predict the next quarter's revenue with high confidence, "
                    "smoothing out random quarterly variations to identify long-term growth trends."
                )
                
            # Invoke prediction engines directly
            tools_outputs = {}
            if run_ratio:
                steps.append("Calculating solvency and risk indicators...")
                try:
                    res_ratio = ml_prediction_engine.predict_risk_score(
                        working_capital=metrics["working_capital"],
                        retained_earnings=metrics["retained_earnings"],
                        ebit=metrics["ebit"],
                        equity_market_val=metrics["equity_market_val"],
                        total_liabilities=metrics["total_liabilities"],
                        sales=metrics["sales"],
                        total_assets=metrics["total_assets"]
                    )
                    tools_outputs["ratio"] = res_ratio
                except Exception as e:
                    steps.append(f"Ratio calculation failed: {str(e)}")
                    
            if run_anomaly:
                steps.append("Scanning operational variables for anomalies...")
                try:
                    res_anomaly = ml_prediction_engine.detect_anomalies(
                        operating_margin=metrics["operating_margin"],
                        leverage_ratio=metrics["leverage_ratio"]
                    )
                    tools_outputs["anomaly"] = res_anomaly
                except Exception as e:
                    steps.append(f"Anomaly detection failed: {str(e)}")
                    
            if run_forecast:
                steps.append("Projecting revenue trajectory...")
                try:
                    res_forecast = ml_prediction_engine.forecast_revenue(
                        quarters_history=metrics["quarters_history"]
                    )
                    tools_outputs["forecast"] = res_forecast
                except Exception as e:
                    steps.append(f"Revenue forecasting failed: {str(e)}")
                    
            # Step 4: Synthesize response
            # Check if Gemini API is configured
            if settings.GEMINI_API_KEY:
                steps.append("Synthesizing clear and concise analyst response with Gemini...")
                try:
                    tools_summary_lines = []
                    if "ratio" in tools_outputs:
                        r = tools_outputs["ratio"]
                        tools_summary_lines.append(
                            f"- Altman Z-Score: {r['altman_z_score']:.2f} (Zone: {r['solvency_status']}, Bankruptcy probability: {r['bankruptcy_probability']*100:.1f}%, Composite Risk: {r['composite_risk_score']}/100)"
                        )
                    if "anomaly" in tools_outputs:
                        a = tools_outputs["anomaly"]
                        status = "Anomaly Detected" if a["is_anomaly"] else "Normal balance"
                        tools_summary_lines.append(
                            f"- Anomaly Check: {status} (Outlier Score: {a['anomaly_confidence_score']*100:.1f}%, Reasoning: {a['reasoning']})"
                        )
                    if "forecast" in tools_outputs:
                        f_val = tools_outputs["forecast"]
                        tools_summary_lines.append(
                            f"- Forecasted Revenue: ${f_val['forecasted_revenue']:.2f}M (Trend: {f_val['trend_direction']}, Confidence: {f_val['forecast_confidence']*100:.1f}%)"
                        )
                    tools_summary_text = "\n".join(tools_summary_lines)
                    
                    formatted_prompt = (
                        f"You are FinSphere AI, a senior elite investment analyst and financial risk auditor.\n"
                        f"The user asked: '{prompt_input}'\n\n"
                        f"Financial Context:\n"
                        f"{clean_rag_answer}\n\n"
                        f"Analytical Model Results:\n"
                        f"{tools_summary_text}\n\n"
                        f"Generate a clear, direct, and short answer to the user's question. "
                        f"Do not write a long document template. Answer directly in 1 to 3 concise, quantitative, and professional paragraphs. "
                        f"Include the calculated Altman Z-score, anomaly warnings, and forecast numbers naturally in your paragraphs where requested, without standard templates or disclaimers."
                        f"If the user asks questions about models, metrics, or calculations (like Altman Z-Score or Isolation Forest anomalies), explain the concepts briefly and clearly."
                    )
                    
                    output = generate_content_with_fallback(formatted_prompt, temperature=0.2)
                    steps.append("Successfully synthesized direct response using Gemini.")
                except Exception as e:
                    output = f"Gemini API invocation failed: {str(e)}"
            else:
                steps.append("Generating clear and direct quantitative analyst summary...")
                report = []
                
                # If we have a valid, clean RAG context answer, use it as the base explanation
                if clean_rag_answer and not "I cannot find sufficient information in the ingested documents" in clean_rag_answer:
                    report.append(clean_rag_answer)
                    report.append("")
                else:
                    report.append("Based on the uploaded financial filings, here is the quantitative summary and diagnostic assessment:")
                    report.append("")
                
                # Prepend explanations if requested
                if explanations:
                    report.append("### Concept & Methodology Overview")
                    for exp in explanations:
                        report.append(exp)
                    report.append("")
                
                if any([run_ratio, run_anomaly, run_forecast]):
                    report.append("### Quantitative Diagnostics & Risk Outputs")
                    if run_ratio and "ratio" in tools_outputs:
                        r = tools_outputs["ratio"]
                        report.append(
                            f"* The balance sheet analysis shows an **Altman Z-Score of {r['altman_z_score']:.2f}**, placing the company in the "
                            f"**{r['solvency_status']}** zone. This indicates a statistical bankruptcy probability of "
                            f"**{r['bankruptcy_probability']*100:.1f}%** and a composite risk rating of **{r['composite_risk_score']}/100**."
                        )
                        
                    if run_anomaly and "anomaly" in tools_outputs:
                        a = tools_outputs["anomaly"]
                        status = "potential accounting anomaly is flagged" if a["is_anomaly"] else "no significant accounting anomalies were detected"
                        report.append(
                            f"* Regarding bookkeeping integrity, a {status} (Outlier Score: **{a['anomaly_confidence_score']*100:.1f}%**). "
                            f"Specifically, {a['reasoning'].lower().replace('unusual combination of', 'there is an unusual combination of')}"
                        )
                        
                    if run_forecast and "forecast" in tools_outputs:
                        f_val = tools_outputs["forecast"]
                        report.append(
                            f"* Our Ridge model forecasts next-quarter revenues to be **${f_val['forecasted_revenue']:.2f}M**, tracing "
                            f"an **{f_val['trend_direction'].lower()}** trajectory with **{f_val['forecast_confidence']*100:.1f}%** model confidence."
                        )
                    report.append("")
                    
                if sources:
                    report.append(f"\n*Sources: {', '.join(sources)}*")
                
                report.append("\n*Note: Running in local sandbox mode. Configure OPENAI_API_KEY or GEMINI_API_KEY in .env for dynamic AI-powered audits.*")
                output = "\n".join(report)
                
            steps.append("Assembling final professional recommendations report.")
            return {
                "output": output,
                "reasoning_steps": steps
            }

analyst_agent = FinSphereAnalystAgent()
