from fastapi import APIRouter, Request
from utilities.utilities import Utilities
import socket

router = APIRouter()

@router.get("/health")
async def health():
    """Health check detalhado com informação do ambiente."""
    return {
        "status": "healthy",
        "environment": Utilities.get_environment_info()
    }

@router.get("/api/debug/environment")
async def debug_environment():
    """Endpoint de debug para ver toda a informação do ambiente."""
    return Utilities.get_environment_info()



@router.get("/")
async def root():
    """Health check básico"""
    return {
        "status": "ok",
        "message": "Crypto Intelligence API - Fase 1",
        "features": [
            "LangChain Agent",
            "Memory System",
            "Custom Tools",
            "Multi-LLM Support"
        ]
    }



@router.get("/debug/connection-info")
async def connection_info(request: Request):
    """Retorna informação sobre a conexão atual"""
    client_ip = request.client.host
    server_ip = socket.gethostbyname(socket.gethostname())
    
    is_tailscale_client = client_ip.startswith('100.') and client_ip.split('.')[1] in [str(i) for i in range(64, 128)]
    is_tailscale_server = server_ip.startswith('100.') and server_ip.split('.')[1] in [str(i) for i in range(64, 128)]
    
    return {
        "client_ip": client_ip,
        "server_ip": server_ip,
        "is_tailscale_client": is_tailscale_client,
        "is_tailscale_server": is_tailscale_server,
        "connection_type": "tailscale" if is_tailscale_client else "local/internet",
        "headers": dict(request.headers)
    }