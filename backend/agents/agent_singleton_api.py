from agents.agent_singleton import agent_manager
from fastapi import APIRouter
from .chat_request import AgentChatRequest
    
router = APIRouter()

@router.post("/api/agent/chat/singleton")
async def agent_chat(request: AgentChatRequest):
    """Chat - usa sempre a LLM atual"""
    agent = agent_manager.get_agent()
    result = agent.run(
        message=request.message,
        conversation_id="test_user_1"
    )
    return result

@router.post("/api/agent/switch-llm")
async def switch_llm(llm_type: str):
    """Troca a LLM globalmente"""
    changed = agent_manager.switch_llm(llm_type)
    return {
        "success": True,
        "changed": changed,
        "current_llm": agent_manager.get_current_llm()
    }

@router.get("/api/agent/current-llm")
async def get_current_llm():
    """Ver qual LLM está ativa"""
    return {"current_llm": agent_manager.get_current_llm()}