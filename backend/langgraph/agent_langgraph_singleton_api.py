# backend/agents/agent_langgraph_api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from .agent_langgraph_singleton import run_langgraph_agent, create_langgraph_agent

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/api/langgraph/singleton", tags=["LangGraph Agent"])

# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    history: List[Message]

# ============================================================================
# AGENT GLOBAL (Singleton)
# ============================================================================

_langgraph_agent = None

def get_langgraph_agent():
    """Obtém ou cria o agent LangGraph"""
    global _langgraph_agent
    
    if _langgraph_agent is None:
        # Importar tools do projeto
        try:
            from tools import get_all_tools
            tools = get_all_tools()
        except:
            # Fallback: sem tools
            tools = []
        
        _langgraph_agent = create_langgraph_agent(tools, verbose=True)
    
    return _langgraph_agent

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/chat", response_model=ChatResponse)
async def chat_with_langgraph(request: ChatRequest):
    """
    Chat com LangGraph agent
    
    - Mantém histórico de conversação
    - Usa ferramentas disponíveis
    - Grafo de estados para decisões
    """
    
    try:
        # Obter agent
        app = get_langgraph_agent()
        
        # Converter history para formato dict
        history_dicts = [msg.dict() for msg in request.history] if request.history else []
        
        # Executar agent
        result = run_langgraph_agent(
            app=app,
            message=request.message,
            conversation_history=history_dicts
        )
        
        # Gerar conversation_id se não existe
        conversation_id = request.conversation_id or f"conv_{hash(request.message)}"
        
        # Converter resposta
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            history=[Message(**msg) for msg in result["history"]]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no LangGraph agent: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Verifica se o LangGraph agent está funcional"""
    
    try:
        agent = get_langgraph_agent()
        return {
            "status": "healthy",
            "agent_type": "LangGraph",
            "graph_compiled": agent is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@router.post("/reset")
async def reset_agent():
    """Reset do agent (força recriação)"""
    
    global _langgraph_agent
    _langgraph_agent = None
    
    return {
        "status": "reset",
        "message": "LangGraph agent será recriado no próximo pedido"
    }

# ============================================================================
# EXEMPLO DE TESTE
# ============================================================================

"""
Exemplo de chamada:

POST http://localhost:8000/api/langgraph/chat
Content-Type: application/json

{
  "message": "Olá! Qual é o preço do Bitcoin?",
  "history": []
}

Resposta:
{
  "response": "O preço atual do Bitcoin é...",
  "conversation_id": "conv_12345",
  "history": [
    {"role": "user", "content": "Olá! Qual é o preço do Bitcoin?"},
    {"role": "assistant", "content": "O preço atual do Bitcoin é..."}
  ]
}
"""