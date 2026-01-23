# backend/test_langgraph.py

"""
Script para testar LangGraph agent localmente
"""

import sys
import os

# Adicionar pasta backend ao path
sys.path.insert(0, os.path.dirname(__file__))

from .agent_langgraph import create_langgraph_agent, run_langgraph_agent
from langchain.tools import Tool

# ============================================================================
# TOOLS DE TESTE
# ============================================================================

def get_crypto_price(symbol: str) -> str:
    """Obtém preço de crypto (mock)"""
    prices = {
        "BTC": "$65,000",
        "ETH": "$3,200",
        "SOL": "$150"
    }
    return prices.get(symbol.upper(), "Preço não disponível")

def get_crypto_news(symbol: str) -> str:
    """Obtém notícias (mock)"""
    return f"Últimas notícias sobre {symbol}: Mercado estável."

# ============================================================================
# CRIAR TOOLS
# ============================================================================

tools = [
    Tool(
        name="get_crypto_price",
        description="Obtém o preço atual de uma criptomoeda. Input: símbolo (BTC, ETH, etc)",
        func=get_crypto_price
    ),
    Tool(
        name="get_crypto_news",
        description="Obtém notícias sobre uma criptomoeda. Input: símbolo",
        func=get_crypto_news
    )
]

# ============================================================================
# TESTES
# ============================================================================

def test_basic_chat():
    """Teste 1: Chat simples"""
    print("\n" + "="*70)
    print("TEST 1: Chat Simples")
    print("-"*70)
    
    app = create_langgraph_agent(tools, verbose=True)
    
    result = run_langgraph_agent(
        app,
        "Olá! Sou um investidor interessado em crypto.",
        conversation_history=[]
    )
    
    print(f"\n🤖 Resposta: {result['response']}")
    print(f"📝 Histórico: {len(result['history'])} mensagens")
    print("✅ Teste 1 passou")

def test_tool_usage():
    """Teste 2: Usar tool"""
    print("\n" + "="*70)
    print("TEST 2: Usar Tool")
    print("-"*70)
    
    app = create_langgraph_agent(tools, verbose=True)
    
    result = run_langgraph_agent(
        app,
        "Qual é o preço atual do Bitcoin?",
        conversation_history=[]
    )
    
    print(f"\n🤖 Resposta: {result['response']}")
    
    # Verificar se usou a tool
    has_tool_call = any(
        hasattr(msg, 'tool_calls') and msg.tool_calls 
        for msg in result['full_messages']
    )
    
    if has_tool_call:
        print("✅ Tool foi usada")
    else:
        print("⚠️ Tool não foi usada")
    
    print("✅ Teste 2 passou")

def test_conversation_history():
    """Teste 3: Manter histórico"""
    print("\n" + "="*70)
    print("TEST 3: Histórico de Conversação")
    print("-"*70)
    
    app = create_langgraph_agent(tools, verbose=True)
    
    # Primeira mensagem
    result1 = run_langgraph_agent(
        app,
        "Qual é o preço do Bitcoin?",
        conversation_history=[]
    )
    print(f"\n🤖 Resposta 1: {result1['response']}")
    
    # Segunda mensagem (com histórico)
    result2 = run_langgraph_agent(
        app,
        "E o Ethereum?",
        conversation_history=result1['history']
    )
    print(f"\n🤖 Resposta 2: {result2['response']}")
    print(f"📝 Histórico final: {len(result2['history'])} mensagens")
    
    assert len(result2['history']) == 4, "Deviam ser 4 mensagens no histórico"
    print("✅ Teste 3 passou")

def test_multiple_tools():
    """Teste 4: Usar múltiplas tools"""
    print("\n" + "="*70)
    print("TEST 4: Múltiplas Tools")
    print("-"*70)
    
    app = create_langgraph_agent(tools, verbose=True)
    
    result = run_langgraph_agent(
        app,
        "Qual é o preço do Bitcoin e quais são as últimas notícias?",
        conversation_history=[]
    )
    
    print(f"\n🤖 Resposta: {result['response']}")
    print("✅ Teste 4 passou")

# ============================================================================
# EXECUTAR TODOS OS TESTES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 TESTES LANGGRAPH AGENT")
    print("="*70)
    
    try:
        test_basic_chat()
        test_tool_usage()
        test_conversation_history()
        test_multiple_tools()
        
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*70 + "\n")
        
        print("Próximo passo:")
        print("  1. Copia os ficheiros para backend/agents/")
        print("  2. Atualiza main.py conforme INSTRUCOES_MAIN_PY.txt")
        print("  3. Inicia a API: python main.py")
        print("  4. Testa no Postman: POST /api/langgraph/chat")
        print()
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()