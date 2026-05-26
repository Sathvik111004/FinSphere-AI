from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.agents.analyst_agent import analyst_agent
from app.database.models import User
from app.api.deps import get_current_user

router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Task prompt for the agent to resolve")
    chat_history: Optional[List[Dict[str, str]]] = None

class AgentResponse(BaseModel):
    output: str
    reasoning_steps: List[str]

@router.post("/run-task", response_model=AgentResponse)
def execute_agent_task(data: AgentRequest, current_user: User = Depends(get_current_user)):
    """
    Executes a structured task utilizing our ReAct financial intelligence agent.
    Returns agent execution pathways and quantitative outputs.
    """
    res = analyst_agent.run_analyst_task(
        prompt_input=data.prompt,
        user_id=current_user.id,
        history=data.chat_history
    )
    return res
