from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import platform
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv()

app = FastAPI()

# CORS para o frontend aceitar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None


def is_running_in_docker() -> bool:
    """
    Deteta se o código está a correr dentro de um container Docker.
    
    Usa múltiplas verificações para maior robustez:
    1. Existência do ficheiro /.dockerenv (método mais comum)
    2. Análise do /proc/1/cgroup (processo init do container)
    3. Variável de ambiente DOCKER_CONTAINER (opcional)
    
    Returns:
        bool: True se estiver em Docker, False caso contrário
    """
    
    # Método 1: Verifica o ficheiro .dockerenv (mais simples e confiável)
    if Path("/.dockerenv").exists():
        return True
    
    # Método 2: Verifica o cgroup (funciona em mais casos)
    try:
        with open("/proc/1/cgroup", "rt") as f:
            content = f.read()
            # Verifica se contém "docker" ou "containerd" no cgroup
            if "docker" in content or "containerd" in content:
                return True
    except Exception:
        # Se não conseguir ler (ex: Windows), ignora
        pass
    
    # Método 3: Variável de ambiente customizada (mais explícito)
    if os.getenv("DOCKER_CONTAINER") == "true":
        return True
    
    # Método 4: Verifica se hostname parece ser de um container
    # Containers costumam ter hostnames hexadecimais curtos
    hostname = platform.node()
    if len(hostname) == 12 and all(c in "0123456789abcdef" for c in hostname):
        return True
    
    return False


def get_ollama_base_url() -> str:
    """
    Determina o URL base do Ollama baseado no ambiente.
    
    Prioridades:
    1. Variável de ambiente OLLAMA_BASE_URL (override manual)
    2. Se estiver em Docker -> host.docker.internal:11434
    3. Caso contrário (desenvolvimento local) -> localhost:11434
    
    Returns:
        str: URL completo do Ollama
    """
    
    # Prioridade 1: Override manual via variável de ambiente
    env_url = os.getenv("OLLAMA_BASE_URL")
    if env_url:
        print(f"📌 [CONFIG] URL do Ollama via env: {env_url}")
        return env_url
    
    # Prioridade 2: Deteta automaticamente o ambiente
    in_docker = is_running_in_docker()
    
    if in_docker:
        url = "http://host.docker.internal:11434"
        print(f"🐳 [DOCKER] Detetado ambiente Docker. URL Ollama: {url}")
        return url
    else:
        url = "http://localhost:11434"
        print(f"💻 [LOCAL] Detetado ambiente local. URL Ollama: {url}")
        return url


def get_environment_info() -> dict:
    """
    Retorna informação detalhada sobre o ambiente de execução.
    Útil para debugging.
    """
    return {
        "running_in_docker": is_running_in_docker(),
        "platform": platform.system(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "ollama_url": get_ollama_base_url(),
        "dockerenv_exists": Path("/.dockerenv").exists(),
        "has_docker_env_var": os.getenv("DOCKER_CONTAINER") is not None,
    }

    
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Endpoint para chat com o Ollama"""
    ollama_url = get_ollama_base_url()
    
    try:
        llm = Ollama(
            model="gpt-oss:120b-cloud",
            base_url=ollama_url
        )
        response = llm.invoke(request.message)
        
        return {
            "response": response,
            "conversation_id": request.conversation_id
        }
    except Exception as e:
        print(f"❌ Erro ao conectar ao Ollama: {str(e)}")
        return {
            "error": f"Erro ao conectar ao Ollama: {str(e)}",
            "ollama_url": ollama_url,
            "suggestion": "Verifica se o Ollama está a correr e se OLLAMA_HOST=0.0.0.0:11434"
        }


@app.get("/api/crypto/{symbol}")
async def get_crypto_price(symbol: str):
    """Endpoint de exemplo para preços de crypto"""
    return {"symbol": symbol, "price": 50000}


@app.get("/")
async def root():
    """Health check básico"""
    return {"status": "ok", "message": "Crypto API running"}


@app.get("/health")
async def health():
    """
    Health check detalhado com informação do ambiente.
    Útil para debugging de problemas de conectividade.
    """
    return {
        "status": "healthy",
        "environment": get_environment_info()
    }


@app.get("/api/debug/environment")
async def debug_environment():
    """
    Endpoint de debug para ver toda a informação do ambiente.
    IMPORTANTE: Desativa isto em produção por segurança!
    """
    return get_environment_info()


# Log de inicialização
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 A iniciar Crypto Intelligence API")
    print("="*60)
    
    env_info = get_environment_info()
    print(f"\n📊 Informação do Ambiente:")
    for key, value in env_info.items():
        print(f"   • {key}: {value}")
    
    print(f"\n🔗 Ollama URL: {get_ollama_base_url()}")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )