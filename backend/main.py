# backend/main.py
from pydantic import BaseModel
from config.llm_config import llm_config

# ✨ Imports do nosso sistema LangChain (Fase 1)
from agents import create_crypto_agent
from api import FastAPIAppFactory
from utilities.utilities import Utilities
from utilities.utilities_api import router as utilities_router


app = FastAPIAppFactory.create_app()


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


# ============================================================================
# AGENT GLOBAL (Fase 1)
# ============================================================================

# Criar agente global (pode ser reconfigurado via endpoints)
crypto_agent = create_crypto_agent(verbose=True)

# ============================================================================
# UTILITIES
# ============================================================================
app.include_router(utilities_router)






# ============================================================================
# ENDPOINTS - CHAT COM AGENT (FASE 1) 🚀
# ============================================================================

@app.post("/api/agent/chat")
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
        result = crypto_agent.run(
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

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Endpoint legacy de chat básico
    Recomenda-se usar /api/agent/chat para funcionalidades completas
    """
    try:
        from langchain_community.llms import Ollama
        
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


@app.get("/api/crypto/{symbol}")
async def get_crypto_price(symbol: str):
    """Endpoint de exemplo para preços de crypto"""
    return {"symbol": symbol, "price": 50000}


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 Crypto Intelligence API - Fase 1")
    print("="*70)
    
    env_info = Utilities.get_environment_info()
    print(f"\n📊 Ambiente:")
    for key, value in env_info.items():
        print(f"   • {key}: {value}")
    
    print(f"\n✨ Novos Endpoints da Fase 1:")
    print(f"   • POST /api/agent/chat - Chat com Agent LangChain")
    print(f"   • GET  /api/agent/conversations - Listar conversas")
    print(f"   • GET  /api/agent/conversation/{{id}}/history - Ver histórico")
    print("="*70 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
