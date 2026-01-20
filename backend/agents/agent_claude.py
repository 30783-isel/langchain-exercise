# backend/agents/agent_claude.py
"""
Agente Claude usando Anthropic
Versão SIMPLES - SEM memory, SEM tools
"""

from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from config.llm_config import llm_config
import os
from dotenv import load_dotenv



class AgentClaude:
    """Agente simples com Claude"""

    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022", verbose: bool = False):
        """Inicializa o agente Claude"""
        try:
            load_dotenv()
            # Criar LLM
            self.llm = ChatAnthropic(
                model=model_name,
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"), 
                temperature=0.7
            )
            
            self.verbose = verbose
            
            if self.verbose:
                print(f"✅ Agent criado com Claude ({model_name})")
                
        except Exception as e:
            print(f"❌ Erro ao criar agent Claude: {e}")
            import traceback
            traceback.print_exc()
            self.llm = None

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
            conversation_id: ID da conversa
            
        Returns:
            Dict com success, response ou error
        """
        if self.llm is None:
            return {
                "success": False,
                "error": "Agente Claude não inicializado",
                "conversation_id": conversation_id
            }

        try:
            # Invocar Claude
            result = self.llm.invoke([HumanMessage(content=message)])
            
            # Extrair resposta
            response = result.content
            
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


def create_claude_agent(verbose: bool = False) -> AgentClaude:
    """Factory function para criar o agente Claude"""
    return AgentClaude(verbose=verbose)