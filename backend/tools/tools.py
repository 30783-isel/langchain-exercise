"""
Tools para o agente LangGraph
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool


def get_all_tools():
    """
    Retorna lista de todas as tools disponíveis para o agente.
    
    Returns:
        list: Lista de tools LangChain
    """
    tools = []
    
    # Tool de pesquisa web
    try:
        search = DuckDuckGoSearchRun()
        search_tool = Tool(
            name="web_search",
            func=search.run,
            description="Pesquisa informação na web. Útil para encontrar informação atual ou factos."
        )
        tools.append(search_tool)
    except Exception as e:
        print(f"Aviso: Não foi possível carregar web_search: {e}")
    
    # Adiciona aqui mais tools conforme necessário
    # Exemplo:
    # tools.append(outra_tool)
    
    return tools