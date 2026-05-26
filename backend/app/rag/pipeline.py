from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.rag.vector_store import vector_store_client

# Explicit QA Prompts forcing source citation and preventing hallucinations
qa_prompt_template = """You are FinSphere AI, a senior elite investment analyst and financial risk auditor. 
You are tasked with providing grounded financial insights.

Review the following retrieved financial context:
---
{context}
---

Answer this query: {question}

Rules for analysis:
1. Ground your response STRICTLY on the retrieved context above. Do not assume or project data.
2. If the context does not contain the answer, state: "I cannot find sufficient information in the ingested documents to answer this query."
3. Cite your sources directly using filenames and page indices if available (e.g. "[Source: report.pdf]").
4. Maintain a professional, quantitative, audit-level tone. Make clear risk assessments.

Your Structured Response:"""

QA_PROMPT = PromptTemplate(
    template=qa_prompt_template, 
    input_variables=["context", "question"]
)

class FinSphereRAGPipeline:
    def __init__(self):
        self.vector_store = vector_store_client.get_vector_store()
        
    def get_llm(self):
        """Resolves active LLM client based on configured environment variables."""
        if settings.OPENAI_API_KEY:
            return ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model="gpt-4o",
                temperature=0.0 # High precision for financial numbers
            )
        else:
            # Safe placeholder LLM when keys are unconfigured, generating high-fidelity mock analyst summaries
            return None

    def query_financial_knowledge(self, query: str, user_id: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Executes a secure multi-step Vector RAG query:
        1. Configures metadata filters to enforce user ownership boundaries.
        2. Retrieves chunks using Maximum Marginal Relevance (MMR) for diversity.
        3. Invokes precision LLM engine.
        """
        # Set up tenant filter boundary
        search_filter = {"user_id": user_id}
        
        # Configure retriever with MMR
        retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 4, 
                "fetch_k": 15,
                "filter": search_filter
            }
        )
        
        # Retrieve chunks
        relevant_docs = retriever.invoke(query)
        
        # Compile context details
        context_blocks = []
        sources = set()
        for doc in relevant_docs:
            context_blocks.append(doc.page_content)
            sources.add(doc.metadata.get("source", "Unknown file"))
            
        combined_context = "\n\n".join(context_blocks)
        
        llm = self.get_llm()
        if llm and combined_context.strip():
            # Run using active LangChain flow (OpenAI)
            try:
                formatted_prompt = QA_PROMPT.format(context=combined_context, question=query)
                response = llm.predict(formatted_prompt)
                answer = response
            except Exception as e:
                answer = f"Error communicating with OpenAI service: {str(e)}"
        elif settings.GEMINI_API_KEY and combined_context.strip():
            # Run using native Google Gemini API
            try:
                import requests
                formatted_prompt = QA_PROMPT.format(context=combined_context, question=query)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [{"text": formatted_prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.0
                    }
                }
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    res_json = response.json()
                    answer = res_json["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    answer = f"Gemini API error (code {response.status_code}): {response.text}"
            except Exception as e:
                answer = f"Error communicating with Gemini service: {str(e)}"
        else:
            # Smart sandbox offline fallback analyzer
            if not combined_context.strip():
                answer = "I cannot find sufficient information in the ingested documents to answer this query. Please ensure appropriate files are uploaded and indexed."
            else:
                answer = f"### Financial Analysis Report\nBased on retrieved records ({', '.join(sources)}), here is the structured summary:\n\n"
                
                # Heuristically parse retrieved context and filter out test-suite metadata
                raw_lines = combined_context.split("\n")
                summary_points = []
                for line in raw_lines:
                    cleaned = line.strip()
                    if len(cleaned) < 20:
                        continue
                    # Clean out test suite tags and boilerplate
                    if any(tag in cleaned for tag in ["Question:", "Expected AI Output:", "Expected Output:", "Expected AI:", "Expected:"]):
                        continue
                    # Remove raw bullet markers
                    for marker in ["-", "*", "•", "▪"]:
                        if cleaned.startswith(marker):
                            cleaned = cleaned[1:].strip()
                    if cleaned and cleaned not in summary_points:
                        summary_points.append(cleaned)
                
                # Take top items and present clearly
                points_to_show = summary_points[:4]
                if not points_to_show:
                    points_to_show = ["Retrieved document contains unstructured raw test templates; please view raw uploaded report files for full details."]
                
                for p in points_to_show:
                    answer += f"- **Key Observation**: {p} [Source: {list(sources)[0]}]\n"
                
                answer += "\n*Note: Running in local sandbox mode. Configure OPENAI_API_KEY or GEMINI_API_KEY in .env for dynamic AI-powered audits.*"
                
        return {
            "answer": answer,
            "sources": list(sources),
            "retrieved_chunks_count": len(relevant_docs)
        }

rag_pipeline = FinSphereRAGPipeline()
