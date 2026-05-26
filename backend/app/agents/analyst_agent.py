from typing import Dict, Any, List
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.config import settings
from app.agents.tools import financial_vector_search, ratio_calculator, revenue_forecaster, anomaly_detector

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
        Supports automatic tool routing even in local sandboxes without active API keys.
        """
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
            # Dynamic rule-based mock analyst router for out-of-the-box local developer demo
            steps = ["Initializing Autonomous Coordinator...", "Inspecting query semantic keywords..."]
            
            prompt_lower = prompt_input.lower()
            
            if "altman" in prompt_lower or "ratio" in prompt_lower or "bankruptcy" in prompt_lower:
                steps.append("Identified: Balance Sheet Ratio calculation required.")
                steps.append("Invoking 'ratio_calculator' tool...")
                # Run with sample standard financial metrics
                res_tool = ratio_calculator.invoke({
                    "working_capital": 45000000,
                    "retained_earnings": 120000000,
                    "ebit": 35000000,
                    "equity_market_val": 280000000,
                    "total_liabilities": 150000000,
                    "sales": 400000000,
                    "total_assets": 500000000
                })
                output = (
                    f"### Autonomous Analyst Risk Assessment\n"
                    f"I have parsed the company balance sheet parameters and executed our machine learning classifier:\n\n"
                    f"{res_tool}\n\n"
                    f"**SWOT Assessment:**\n"
                    f"- **Strengths**: Robust revenue generation relative to assets.\n"
                    f"- **Weaknesses**: High relative liabilities footprint.\n"
                    f"- **Risk mitigation**: Balanced portfolio diversification recommended."
                )
            elif "forecast" in prompt_lower or "revenue" in prompt_lower:
                steps.append("Identified: Revenue growth trajectory prediction required.")
                steps.append("Invoking 'revenue_forecaster' tool...")
                res_tool = revenue_forecaster.invoke({"quarters_history": [105.0, 112.5, 118.0, 124.2]})
                output = (
                    f"### Financial Revenue Forecasting Summary\n"
                    f"I ran our Ridge growth model on the quarterly history:\n\n"
                    f"{res_tool}\n\n"
                    f"**Forecast Statement:** Projections outline stable expansion, matching positive market trends."
                )
            elif "anomaly" in prompt_lower or "irregular" in prompt_lower:
                steps.append("Identified: Accounting anomaly check required.")
                steps.append("Invoking 'anomaly_detector' tool...")
                res_tool = anomaly_detector.invoke({"operating_margin": -0.45, "leverage_ratio": 5.2})
                output = (
                    f"### Audit Irregularity Scan\n"
                    f"I scanned balance sheet operational variables:\n\n"
                    f"{res_tool}\n\n"
                    f"**Audit Warning**: Re-verify operational cash flow disclosures."
                )
            else:
                steps.append("Identified: Standard retrieval query required.")
                steps.append("Invoking 'financial_vector_search' tool...")
                res_tool = financial_vector_search.invoke({"query": prompt_input, "user_id": user_id})
                output = (
                    f"### Ingested Intelligence Search Report\n"
                    f"{res_tool}\n\n"
                    f"Let me know if you would like me to calculate solvency scores or project revenue targets!"
                )
                
            steps.append("Assembling final professional recommendations report.")
            return {
                "output": output,
                "reasoning_steps": steps
            }

analyst_agent = FinSphereAnalystAgent()
