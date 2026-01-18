# backend/agents/crypto_agent.py
"""
Agente Principal de Crypto Intelligence
Usa LLM, Memory e Tools para responder perguntas sobre crypto
"""
from typing import Optional, Dict, Any


from config.llm_config import get_default_llm
from memory.conversation_memory import get_memory
from tools.crypto_tools import get_all_tools


# Prompt template para o agente
CRYPTO_AGENT_PROMPT = """Você é um assistente especializado em criptomoedas.
Você tem acesso às seguintes ferramentas:

{tools}

Descrição das ferramentas:
{tool_names}

Use o seguinte formato:

Question: a pergunta que você deve responder
Thought: você deve sempre pensar sobre o que fazer
Action: a ação a tomar, deve ser uma de [{tool_names}]
Action Input: o input para a ação
Observation: o resultado da ação
... (este Thought/Action/Action Input/Observation pode repetir N vezes)
Thought: Eu agora sei a resposta final
Final Answer: a resposta final à pergunta original

IMPORTANTE:
- Seja sempre prestável e educativo
- Para dados de mercado, use as ferramentas disponíveis
- Admita quando não tem informação suficiente
- Sugira onde o utilizador pode encontrar mais informação

Histórico da conversa:
{chat_history}

Pergunta: {input}
{agent_scratchpad}
"""


class CryptoAgent:
    """
    Agente conversacional para análise de criptomoedas
    Combina LLM + Memory + Tools
    """
    
    def __init__(
        self,
        llm=None,
        memory_type: str = "buffer",
        verbose: bool = True
    ):
        """
        Inicializa o agente
        
        Args:
            llm: Instância de LLM (usa default se None)
            memory_type: Tipo de memória a usar
            verbose: Se deve mostrar raciocínio do agente
        """
        self.llm = llm or get_default_llm()
        self.memory_type = memory_type
        self.verbose = verbose
        self.tools = get_all_tools()
        
        # Criar prompt
        self.prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad", "chat_history", "tools", "tool_names"],
            template=CRYPTO_AGENT_PROMPT
        )
        
        # Criar o agente base
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
    
    def create_executor(self, conversation_id: str) -> AgentExecutor:
        """
        Cria executor do agente com memória para uma conversa específica
        
        Args:
            conversation_id: ID único da conversa
        """
        memory = get_memory(
            conversation_id,
            memory_type=self.memory_type,
            llm=self.llm
        )
        
        executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=memory,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=5
        )
        
        return executor
    
    def run(
        self,
        message: str,
        conversation_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Executa o agente com uma mensagem
        
        Args:
            message: Mensagem do utilizador
            conversation_id: ID da conversa
            **kwargs: Argumentos adicionais
        
        Returns:
            Dict com resposta e metadata
        """
        try:
            executor = self.create_executor(conversation_id)
            
            # Invocar o agente
            result = executor.invoke({"input": message})
            
            return {
                "success": True,
                "response": result["output"],
                "conversation_id": conversation_id,
                "intermediate_steps": result.get("intermediate_steps", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }
    
    async def arun(
        self,
        message: str,
        conversation_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Versão assíncrona do run
        Para usar com FastAPI async endpoints
        """
        # Por agora, chama a versão síncrona
        # Na Fase 4/5 podemos otimizar para async real
        return self.run(message, conversation_id, **kwargs)


def create_crypto_agent(**kwargs) -> CryptoAgent:
    """
    Factory function para criar agente
    
    Uso:
        from agents.crypto_agent import create_crypto_agent
        agent = create_crypto_agent(verbose=True)
        result = agent.run("Qual é o preço do Bitcoin?", "user_123")
    """
    return CryptoAgent(**kwargs)
