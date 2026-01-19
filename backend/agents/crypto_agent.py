# backend/agents/crypto_agent.py
"""
Agente Principal de Crypto Intelligence
Versão SIMPLES usando LangChain 1.2.x `create_agent`
SEM memory, SEM tools - apenas LLM
"""

from typing import Dict, Any
from langchain.agents import create_agent
from langchain_community.llms import Ollama
from config.llm_config import llm_config


class CryptoAgent:
    """
    Agente simples sem memory nem tools
    Perfeito para testes básicos
    """

    def __init__(self, model_name: str = "gpt-oss:120b-cloud", verbose: bool = False):
        """Inicializa o agente"""
        try:
            # Criar LLM
            self.llm = Ollama(
                model=model_name,
                base_url=llm_config.ollama_url
            )
            
            # Criar agent (versão simples)
            self.agent = create_agent(
                model=self.llm,
                tools=[]  # Sem tools por agora
            )
            
            self.verbose = verbose
            
            if self.verbose:
                print(f"✅ Agent criado com Ollama ({model_name})")
                
        except Exception as e:
            print(f"❌ Erro ao criar agent: {e}")
            import traceback
            traceback.print_exc()
            self.agent = None

    def run(
        self, 
        message: str, 
        conversation_id: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Executa o agente
        
        Args:
            message: Pergunta do utilizador
            conversation_id: ID da conversa (ignorado nesta versão simples)
            
        Returns:
            Dict com success, response ou error
        """
        if self.agent is None:
            return {
                "success": False,
                "error": "Agente não inicializado",
                "conversation_id": conversation_id
            }

        try:
            # Invocar agent
            result = self.agent.invoke({
                "messages": [{"role": "user", "content": message}]
            })
            
            # Extrair resposta
            if isinstance(result, dict):
                response = result.get("output", str(result))
            else:
                response = str(result)
            
            return {
                "success": True,
                "response": response,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }


def create_crypto_agent(**kwargs) -> CryptoAgent:
    """Factory function para criar agente"""
    return CryptoAgent(**kwargs)


