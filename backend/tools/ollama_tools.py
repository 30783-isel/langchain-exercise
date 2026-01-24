"""
Helper para bind de tools com ChatOllama
"""

from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool


# backend/tools/ollama_tools.py

from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool


def bind_tools_ollama(llm, tools):
    """
    Faz bind de tools para ChatOllama usando formato JSON.
    Requer modelo compatível (llama3.1+, mistral, etc)
    
    Args:
        llm: ChatOllama instance
        tools: Lista de tools
        
    Returns:
        LLM com tools em formato JSON
    """
    # Converter tools para formato OpenAI (JSON)
    tools_json = [convert_to_openai_tool(tool) for tool in tools]
    
    # Bind usando formato JSON (SEM tool_choice - não suportado)
    llm_with_tools = llm.bind(tools=tools_json)
    
    return llm_with_tools