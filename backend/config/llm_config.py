# backend/config/llm_config.py
"""
Configuração centralizada para LLMs (OpenAI, Ollama)
"""
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

load_dotenv()


def is_running_in_docker() -> bool:
    """Deteta se está a correr em Docker"""
    if Path("/.dockerenv").exists():
        return True
    try:
        with open("/proc/1/cgroup", "rt") as f:
            return "docker" in f.read() or "containerd" in f.read()
    except Exception:
        return False


def get_ollama_url() -> str:
    """Retorna URL do Ollama baseado no ambiente"""
    env_url = os.getenv("OLLAMA_BASE_URL")
    if env_url:
        return env_url
    
    return "http://host.docker.internal:11434" if is_running_in_docker() else "http://localhost:11434"


class LLMConfig:
    """Classe para gerir configuração de LLMs"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.ollama_url = get_ollama_url()
        self.default_model = os.getenv("DEFAULT_LLM", "ollama")
        
    def get_llm(self, model_type: Optional[str] = None, **kwargs):
        """
        Retorna uma instância de LLM configurada
        
        Args:
            model_type: "openai" ou "ollama" (usa default se None)
            **kwargs: Argumentos adicionais para o LLM
        """
        llm_type = model_type or self.default_model
        
        if llm_type == "openai":
            return self._get_openai_llm(**kwargs)
        elif llm_type == "ollama":
            return self._get_ollama_llm(**kwargs)
        else:
            raise ValueError(f"Tipo de LLM não suportado: {llm_type}")
    
    def _get_openai_llm(self, **kwargs):
        """Configura OpenAI LLM"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não configurada no .env")
        
        default_params = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "api_key": self.openai_api_key
        }
        default_params.update(kwargs)
        
        return ChatOpenAI(**default_params)
    
    def _get_ollama_llm(self, **kwargs):
        """Configura Ollama LLM"""
        default_params = {
            "model": "gpt-oss:120b-cloud",
            "base_url": self.ollama_url,
            "temperature": 0.7
        }
        default_params.update(kwargs)
        
        return Ollama(**default_params)


# Instância global para facilitar imports
llm_config = LLMConfig()


def get_default_llm(**kwargs):
    """
    Função de conveniência para obter LLM default
    
    Uso:
        from config.llm_config import get_default_llm
        llm = get_default_llm(temperature=0.5)
    """
    return llm_config.get_llm(**kwargs)
