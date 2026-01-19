# test_langchain_v1.2.py
"""
Script de validação para LangChain 1.2.x
Testa que todas as mudanças estão corretas
"""

from config.llm_config import llm_config


print("\n" + "="*70)
print("🧪 VALIDAÇÃO LANGCHAIN 1.2.x")
print("="*70 + "\n")

# ============================================================================
# TESTE 1: Verificar Versões
# ============================================================================
print("📦 TESTE 1: Verificar Versões Instaladas")
print("-"*70)

try:
    import langchain
    import langchain_core
    import langchain_community
    
    print(f"✅ langchain: {langchain.__version__}")
    print(f"✅ langchain-core: {langchain_core.__version__}")
    print(f"✅ langchain-community: {langchain_community.__version__}")
    
    # Verificar se é 1.2.x
    lc_version = tuple(map(int, langchain.__version__.split('.')[:2]))
    if lc_version >= (1, 2):
        print(f"\n✅ LangChain {langchain.__version__} é compatível!")
    else:
        print(f"\n⚠️ LangChain {langchain.__version__} pode ter problemas")
        print("   Recomendado: >= 1.2.0")
        
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    print("\nInstala: pip install langchain langchain-core langchain-community")
    exit(1)


# ============================================================================
# TESTE 2: Criar Agent Simples
# ============================================================================
print("\n" + "="*70)
print("🤖 TESTE 3: Criar Agent com API 1.2.x")
print("-"*70)

try:

    from langchain.agents import create_agent
    from langchain_openai import ChatOpenAI
    from langchain_community.llms import Ollama
    
    llm = Ollama(
        model="gpt-oss:120b-cloud",
        base_url=llm_config.ollama_url
    )
    response = llm.invoke('O que é um leptão')
        
    model = ChatOpenAI(
        model="gpt-5",
        temperature=0.1,
        max_tokens=1000,
        timeout=30
    )
    agent = create_agent(model)
    
except Exception as e:
    print(f"❌ Erro ao criar agent: {e}")
    import traceback
    traceback.print_exc()




# ============================================================================ 
# TESTE 3: Criar Agent Simples usando CryptoAgent
# ============================================================================
print("\n" + "="*70)
print("🤖 TESTE 3: Criar Agent com classe CryptoAgent")
print("-"*70)

try:
    from backend.agents.crypto_agent import create_crypto_agent
    from config import llm_config  # Para obter ollama_url
    
    # Criar a instância do agente
    agent = create_crypto_agent()
    
    # Mensagem de teste
    message = "Resumidamente, o que é um leptão?"
    
    # Contexto opcional, podemos passar kwargs se necessário
    result = agent.run(
        message=message,
        conversation_id="test_user_1"
    )
    
    # Mostrar resultado
    if result["success"]:
        print(f"\n✅ Agent respondeu com sucesso:\n{result['response']}")
    else:
        print(f"\n❌ Erro na execução do agente: {result['error']}")
    
except Exception as e:
    print(f"❌ Erro ao criar ou executar o CryptoAgent: {e}")
    import traceback
    traceback.print_exc()
