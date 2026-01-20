from .crypto_agent import CryptoAgent
 
class CryptoAgentSingleton:
    """Singleton mutável - permite trocar LLM globalmente"""
    
    _instance = None
    _current_agent = None
    _current_llm_type = "ollama"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_agent(self) -> CryptoAgent:
        """Retorna o agent atual"""
        if self._current_agent is None:
            self._current_agent = CryptoAgent(model_name="gpt-oss:120b-cloud")
        return self._current_agent
    
    def switch_llm(self, llm_type: str) -> bool:
        """Troca o LLM globalmente"""
        if llm_type == self._current_llm_type:
            return False  # Já está a usar esta LLM
        
        if llm_type == "claude":
            self._current_agent = CryptoAgent(model_name="claude-sonnet-4")
        elif llm_type == "ollama":
            self._current_agent = CryptoAgent(model_name="gpt-oss:120b-cloud")
        else:
            raise ValueError(f"LLM desconhecida: {llm_type}")
        
        self._current_llm_type = llm_type
        return True
    
    def get_current_llm(self) -> str:
        """Retorna qual LLM está ativa"""
        return self._current_llm_type


# Instância global
agent_manager = CryptoAgentSingleton()