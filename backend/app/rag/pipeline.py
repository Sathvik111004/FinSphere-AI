from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.rag.vector_store import vector_store_client
from app.utils.gemini import generate_content_with_fallback

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
            # Run using native Google Gemini API with robust fallbacks and retries
            try:
                formatted_prompt = QA_PROMPT.format(context=combined_context, question=query)
                answer = generate_content_with_fallback(formatted_prompt, temperature=0.0)
            except Exception as e:
                answer = f"Error communicating with Gemini service: {str(e)}"
        else:
            # Smart sandbox offline fallback analyzer
            if not combined_context.strip():
                answer = "I cannot find sufficient information in the ingested documents to answer this query. Please ensure appropriate files are uploaded and indexed."
            else:
                answer = f"### Financial Analysis Report\nBased on retrieved records ({', '.join(sources)}), here is the structured summary:\n\n"
                
                import re
                
                # 1. Reconstruct paragraphs by joining single newlines only when they represent wrapped text
                lines = combined_context.split("\n")
                reconstructed_blocks = []
                current_block = ""
                for line in lines:
                    line_strip = line.strip()
                    if not line_strip:
                        if current_block:
                            reconstructed_blocks.append(current_block)
                            current_block = ""
                        continue
                    
                    if current_block:
                        ends_with_terminator = current_block.rstrip()[-1] in ".!?"
                        starts_new_field = (
                            line_strip[0].isupper() or 
                            line_strip[0].isdigit() or 
                            line_strip[0] in "-*•▪" or 
                            (":" in line_strip and len(line_strip.split(":")[0]) < 25)
                        )
                        if not ends_with_terminator and not starts_new_field:
                            current_block = current_block.rstrip() + " " + line_strip
                            continue
                    
                    if current_block:
                        reconstructed_blocks.append(current_block)
                    current_block = line_strip
                
                if current_block:
                    reconstructed_blocks.append(current_block)
                
                # 2. Extract clean sentences from each reconstructed block
                summary_points = []
                for block in reconstructed_blocks:
                    for sentence in re.split(r'(?<=[.!?])\s+', block):
                        cleaned = sentence.strip()
                        if len(cleaned) < 15:
                            continue
                        # Filter out dividing lines (consisting of repeating symbols like =, -, *, _)
                        if len(set(cleaned)) <= 4 and any(c in "-=_*·•▪ " for c in cleaned):
                            continue
                        # Clean out test suite tags and boilerplate
                        if any(tag in cleaned for tag in ["Question:", "Expected AI Output:", "Expected Output:", "Expected AI:", "Expected:"]):
                            continue
                        # Remove any leading bullet or list markers
                        cleaned = re.sub(r'^[-*•▪\d\.\s]+', '', cleaned).strip()
                        
                        if cleaned and cleaned not in summary_points:
                            summary_points.append(cleaned)
                
                # Rank summary points based on query similarity
                # Split query into lowercase alphanumeric words, filtering out common stopwords
                stopwords = {
                    "what", "is", "the", "are", "of", "in", "about", "on", "for", "with", "a", "an", "to", "and", 
                    "or", "by", "from", "at", "how", "why", "where", "who", "which", "do", "does", "did", "can",
                    "could", "should", "would", "will", "shall", "me", "my", "our", "your", "his", "her", "their",
                    "was", "were", "been", "has", "have", "had", "be", "than", "more", "less", "least"
                }
                query_words = [w.strip().lower() for w in re.split(r'\W+', query) if w.strip()]
                query_keywords = [w for w in query_words if w not in stopwords and len(w) > 1]
                
                # Build roots of query words to handle plurals/conjugations (e.g. "founded" matches "found")
                query_roots = set()
                for kw in query_keywords:
                    query_roots.add(kw)
                    if kw.endswith("ed"):
                        query_roots.add(kw[:-2])
                        query_roots.add(kw[:-1])
                    if kw.endswith("ing"):
                        query_roots.add(kw[:-3])
                    if kw.endswith("s") and len(kw) > 3:
                        query_roots.add(kw[:-1])
                
                ranked_points = []
                for point in summary_points:
                    point_lower = point.lower()
                    score = 0
                    
                    # Score keyword matches
                    for kw in query_keywords:
                        if re.search(r'\b' + re.escape(kw) + r'\b', point_lower):
                            score += 3
                        elif kw in point_lower:
                            score += 1
                            
                    # Penalize unrelated tabular fields (e.g., "Founded: 2008") if the user did not query them
                    tabular_keys = ["founded", "headquarters", "employees", "industry", "headquarter", "employee"]
                    for tk in tabular_keys:
                        if tk in point_lower:
                            user_asked = any((kw in tk or tk in kw) for kw in query_roots)
                            if not user_asked:
                                score -= 10
                                
                    ranked_points.append((score, point))
                
                # Sort by score descending
                ranked_points.sort(key=lambda x: x[0], reverse=True)
                
                # Take top items and present clearly
                matching_points = [p[1] for p in ranked_points if p[0] > 0]
                if matching_points:
                    points_to_show = matching_points[:4]
                else:
                    points_to_show = [p[1] for p in ranked_points[:4]]
                
                if not points_to_show:
                    points_to_show = ["Retrieved document contains unstructured raw test templates; please view raw uploaded report files for full details."]
                
                for p in points_to_show:
                    answer += f"- {p} [Source: {list(sources)[0]}]\n"
                
                answer += "\n*Note: Running in local sandbox mode. Configure OPENAI_API_KEY or GEMINI_API_KEY in .env for dynamic AI-powered audits.*"
                
        return {
            "answer": answer,
            "sources": list(sources),
            "retrieved_chunks_count": len(relevant_docs)
        }

rag_pipeline = FinSphereRAGPipeline()
