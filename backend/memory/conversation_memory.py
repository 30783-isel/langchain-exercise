# backend/memory/conversation_memory.py
"""
Sistema de memória conversacional para o agente
Suporta múltiplos tipos de memória do LangChain
"""
from typing import Optional, Dict
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain.memory.chat_memory import BaseChatMemory


class MemoryManager:
    """
    Gestor de memória para conversas com o agente
    Permite trocar entre diferentes tipos de memória
    """
    
    def __init__(self):
        self.conversations: Dict[str, BaseChatMemory] = {}
    
    def get_memory(
        self, 
        conversation_id: str,
        memory_type: str = "buffer",
        llm=None,
        **kwargs
    ) -> BaseChatMemory:
        """
        Retorna ou cria memória para uma conversa
        
        Args:
            conversation_id: ID único da conversa
            memory_type: Tipo de memória ("buffer", "window", "summary")
            llm: LLM para usar (necessário para summary)
            **kwargs: Argumentos adicionais para o tipo de memória
        """
        # Se já existe, retorna
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]
        
        # Criar nova memória baseada no tipo
        memory = self._create_memory(memory_type, llm, **kwargs)
        self.conversations[conversation_id] = memory
        
        return memory
    
    def _create_memory(
        self, 
        memory_type: str,
        llm=None,
        **kwargs
    ) -> BaseChatMemory:
        """Cria instância de memória baseada no tipo"""
        
        if memory_type == "buffer":
            # Guarda todas as mensagens
            return ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                **kwargs
            )
        
        elif memory_type == "window":
            # Guarda apenas últimas K mensagens
            k = kwargs.pop("k", 5)
            return ConversationBufferWindowMemory(
                k=k,
                memory_key="chat_history",
                return_messages=True,
                **kwargs
            )
        
        elif memory_type == "summary":
            # Resume conversas longas
            if not llm:
                raise ValueError("LLM necessário para ConversationSummaryMemory")
            
            return ConversationSummaryMemory(
                llm=llm,
                memory_key="chat_history",
                return_messages=True,
                **kwargs
            )
        
        else:
            raise ValueError(f"Tipo de memória não suportado: {memory_type}")
    
    def clear_conversation(self, conversation_id: str):
        """Limpa memória de uma conversa específica"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id].clear()
    
    def delete_conversation(self, conversation_id: str):
        """Remove conversa completamente"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
    
    def get_conversation_history(self, conversation_id: str) -> list:
        """Retorna histórico de mensagens de uma conversa"""
        if conversation_id not in self.conversations:
            return []
        
        memory = self.conversations[conversation_id]
        return memory.chat_memory.messages
    
    def list_conversations(self) -> list:
        """Lista todas as conversas ativas"""
        return list(self.conversations.keys())


# Instância global do gestor de memória
memory_manager = MemoryManager()


def get_memory(conversation_id: str, **kwargs) -> BaseChatMemory:
    """
    Função de conveniência para obter memória
    
    Uso:
        from memory.conversation_memory import get_memory
        memory = get_memory("user_123", memory_type="buffer")
    """
    return memory_manager.get_memory(conversation_id, **kwargs)
