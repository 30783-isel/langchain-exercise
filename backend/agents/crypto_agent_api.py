from fastapi import APIRouter
from pydantic import BaseModel
from agents.crypto_agent import agent
from config.llm_config import llm_config
from langchain_community.llms import Ollama
# ============================================================================
# ENDPOINTS - CHAT COM AGENT (FASE 1) 🚀
# ============================================================================

router = APIRouter()

# ============================================================================
# MODELS
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"


class AgentChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"
    memory_type: str = "buffer"  # "buffer", "window", "summary"
    verbose: bool = False
    
@router.post("/api/agent/chat")
async def agent_chat(request: AgentChatRequest):
    """
    ✨ NOVO - Endpoint para chat com o LangChain Agent
    
    Suporta:
    - Memória conversacional
    - Uso de ferramentas (tools)
    - Raciocínio via ReAct pattern
    
    Fase 1 Completa!
    """
    try:
        # Executar o agente
        result = agent.run(
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        if result["success"]:
            return {
                "response": result["response"],
                "conversation_id": result["conversation_id"],
                "success": True,
                "phase": "Fase 1 - Agent + Memory + Tools"
            }
        else:
            return {
                "error": result["error"],
                "conversation_id": result["conversation_id"],
                "success": False
            }
            
    except Exception as e:
        return {
            "error": f"Erro ao processar mensagem: {str(e)}",
            "success": False
        }





# ============================================================================
# ENDPOINTS - LEGACY (mantidos para compatibilidade)
# ============================================================================

@router.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Endpoint legacy de chat básico
    Recomenda-se usar /api/agent/chat para funcionalidades completas
    """
    try:
        llm = Ollama(
            model="gpt-oss:120b-cloud",
            base_url=llm_config.ollama_url
        )
        response = llm.invoke(request.message)
        
        return {
            "response": response,
            "conversation_id": request.conversation_id,
            "note": "Use /api/agent/chat para funcionalidades avançadas"
        }
    except Exception as e:
        return {
            "error": f"Erro ao conectar ao Ollama: {str(e)}",
            "ollama_url": llm_config.ollama_url
        }


@router.get("/api/crypto/{symbol}")
async def get_crypto_price(symbol: str):
    """Endpoint de exemplo para preços de crypto"""
    return {"symbol": symbol, "price": 50000}