from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.rag.pipeline import rag_pipeline
from app.database.models import User
from app.api.deps import get_current_user

router = APIRouter()

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Q&A query search string")

class QueryResponse(BaseModel):
    answer: str
    sources: List[str] = []
    retrieved_chunks_count: int

@router.post("/query", response_model=QueryResponse)
def query_rag(data: QueryRequest, current_user: User = Depends(get_current_user)):
    """
    Interfaces with the grounded vector RAG pipeline.
    Uses tenant boundaries to prevent cross-user document lookups.
    """
    res = rag_pipeline.query_financial_knowledge(
        query=data.query,
        user_id=current_user.id
    )
    return res
