# backend/main.py

# ✨ Imports do nosso sistema LangChain (Fase 1)
from api import FastAPIAppFactory
from utilities.utilities import Utilities
from utilities.utilities_api import router as utilities_router
from agents.agent_ollama_api import router as crypto_agent_router
from agents.agent_singleton_api import router as agent_singleton_router
from langgraph.agent_langgraph_api import router as langgraph_router
from langgraph.agent_langgraph_singleton_api import router as langgraph_singleton_router

app = FastAPIAppFactory.create_app()

# ============================================================================
# APIs
# ============================================================================
app.include_router(utilities_router)
app.include_router(crypto_agent_router)
app.include_router(agent_singleton_router)
app.include_router(langgraph_router)
app.include_router(langgraph_singleton_router)

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
    
    # No print de endpoints, adiciona:
    print(f"\n✨ Endpoints LangGraph:")
    print(f"   • POST /api/langgraph/chat - Chat com LangGraph")
    print(f"   • GET  /api/langgraph/health - Health check")
    print(f"   • POST /api/langgraph/reset - Reset agent")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
