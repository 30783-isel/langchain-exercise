# backend/agents/agent_langgraph.py

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import operator
from agents.agent_singleton import CryptoAgentSingleton

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from tools.ollama_tools import bind_tools_ollama

# ============================================================================
# ESTADO DO AGENT
# ============================================================================

class AgentState(TypedDict):
    """Estado do agent LangGraph"""
    messages: Annotated[Sequence[BaseMessage], operator.add]

# ============================================================================
# FUNÇÕES DO GRAFO
# ============================================================================

def should_continue(state: AgentState) -> str:
    """Decide se deve continuar ou terminar"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return END

def call_model(state: AgentState, llm):
    """Chama o modelo LLM do singleton"""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# ============================================================================
# CRIAR GRAFO LANGGRAPH
# ============================================================================

def create_langgraph_agent(tools: list, verbose: bool = False):
    """
    Cria um agent usando LangGraph com LLM dinâmica do singleton
    
    Args:
        tools: Lista de tools LangChain
        verbose: Se True, mostra debug info
    
    Returns:
        Grafo compilado pronto a usar
    """
    
    # 1. Obter LLM do singleton
    agent_singleton = CryptoAgentSingleton()
    agent = agent_singleton.get_agent()
    llm = agent.llm  # LLM dinâmica (Ollama ou Claude)
        # Verificar tipo de LLM e fazer bind apropriado
    if isinstance(llm, ChatAnthropic):
        # Claude suporta bind_tools nativamente
        llm_with_tools = llm.bind_tools(tools)
    elif isinstance(llm, ChatOllama):
        # Ollama precisa de formato JSON
        llm_with_tools = bind_tools_ollama(llm, tools)
    else:
        raise ValueError(f"LLM tipo {type(llm)} não suportado")
    
    return llm_with_tools

    
    # 2. Criar grafo
    workflow = StateGraph(AgentState)
    
    # 3. Adicionar nós
    workflow.add_node("agent", lambda state: call_model(state, llm_with_tools))
    workflow.add_node("tools", ToolNode(tools))
    
    # 4. Definir entry point
    workflow.set_entry_point("agent")
    
    # 5. Adicionar edges condicionais
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # 6. Adicionar edge de tools de volta para agent
    workflow.add_edge("tools", "agent")
    
    # 7. Compilar
    app = workflow.compile()
    
    if verbose:
        current_llm = agent_singleton.get_current_llm()
        print(f"✅ LangGraph agent criado com {current_llm}")
        print(f"   • Nós: agent, tools")
        print(f"   • Tools disponíveis: {len(tools)}")
    
    return app

# ============================================================================
# EXECUTAR AGENT
# ============================================================================

def run_langgraph_agent(app, message: str, conversation_history: list = None):
    """
    Executa o agent LangGraph
    
    Args:
        app: Grafo LangGraph compilado
        message: Mensagem do utilizador
        conversation_history: Histórico opcional (lista de dicts)
    
    Returns:
        dict com resposta e histórico
    """
    
    # Converter histórico para mensagens LangChain
    messages = []
    if conversation_history:
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
    
    # Adicionar mensagem atual
    messages.append(HumanMessage(content=message))
    
    # Executar grafo
    result = app.invoke({"messages": messages})
    
    # Extrair resposta
    last_message = result["messages"][-1]
    response_text = last_message.content
    
    # Construir histórico atualizado
    updated_history = conversation_history or []
    updated_history.append({"role": "user", "content": message})
    updated_history.append({"role": "assistant", "content": response_text})
    
    return {
        "response": response_text,
        "history": updated_history,
        "full_messages": result["messages"]
    }

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    from langchain.tools import Tool
    
    def get_crypto_price(symbol: str) -> str:
        """Obtém preço de crypto (exemplo)"""
        return f"BTC está a ${50000}"
    
    tools = [
        Tool(
            name="get_crypto_price",
            description="Obtém o preço atual de uma criptomoeda",
            func=get_crypto_price
        )
    ]
    
    # Criar agent (usa LLM do singleton)
    app = create_langgraph_agent(tools, verbose=True)
    
    # Trocar LLM se quiseres
    # agent_singleton = CryptoAgentSingleton()
    # agent_singleton.switch_llm("claude")
    
    # Testar
    result = run_langgraph_agent(
        app,
        "Qual é o preço do Bitcoin?",
        conversation_history=[]
    )
    
    print(f"\n🤖 Resposta: {result['response']}")