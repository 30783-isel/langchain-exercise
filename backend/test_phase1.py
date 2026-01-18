# backend/test_phase1.py
"""
Script de teste para validar a Fase 1
Exemplos de uso do Agent, Memory e Tools
"""
import asyncio
from agents.crypto_agent import create_crypto_agent
from memory.conversation_memory import memory_manager
from config.llm_config import llm_config


def test_agent_basic():
    """Teste 1: Agent básico sem memória"""
    print("\n" + "="*70)
    print("🧪 TESTE 1: Agent Básico")
    print("="*70)
    
    agent = create_crypto_agent(verbose=True)
    
    result = agent.run(
        message="Olá! Qual é o preço do Bitcoin?",
        conversation_id="test_1"
    )
    
    print(f"\n✅ Resposta: {result['response']}")
    print(f"🆔 Conversa: {result['conversation_id']}")


def test_agent_with_tools():
    """Teste 2: Agent usando ferramentas"""
    print("\n" + "="*70)
    print("🧪 TESTE 2: Agent com Ferramentas")
    print("="*70)
    
    agent = create_crypto_agent(verbose=True)
    
    # Pergunta que deve acionar a ferramenta crypto_price_simulator
    result = agent.run(
        message="Mostra-me dados de preço do Ethereum nos últimos 7 dias",
        conversation_id="test_2"
    )
    
    print(f"\n✅ Resposta: {result['response']}")


def test_agent_with_memory():
    """Teste 3: Agent com memória conversacional"""
    print("\n" + "="*70)
    print("🧪 TESTE 3: Agent com Memória")
    print("="*70)
    
    agent = create_crypto_agent(verbose=False)  # Menos verbose
    
    conv_id = "test_memory"
    
    # Primeira mensagem
    print("\n📨 Mensagem 1:")
    result1 = agent.run(
        message="O meu nome é João e tenho interesse em Bitcoin",
        conversation_id=conv_id
    )
    print(f"🤖 Resposta: {result1['response']}")
    
    # Segunda mensagem (deve lembrar do nome)
    print("\n📨 Mensagem 2:")
    result2 = agent.run(
        message="Qual é o meu nome?",
        conversation_id=conv_id
    )
    print(f"🤖 Resposta: {result2['response']}")
    
    # Ver histórico
    history = memory_manager.get_conversation_history(conv_id)
    print(f"\n📜 Histórico: {len(history)} mensagens")


def test_memory_types():
    """Teste 4: Diferentes tipos de memória"""
    print("\n" + "="*70)
    print("🧪 TESTE 4: Tipos de Memória")
    print("="*70)
    
    # Buffer Memory (guarda tudo)
    print("\n1️⃣ Buffer Memory:")
    agent_buffer = create_crypto_agent(verbose=False)
    agent_buffer.memory_type = "buffer"
    
    result = agent_buffer.run(
        message="Teste buffer memory",
        conversation_id="test_buffer"
    )
    print(f"✅ Buffer: {result['success']}")
    
    # Window Memory (últimas K mensagens)
    print("\n2️⃣ Window Memory (k=3):")
    agent_window = create_crypto_agent(verbose=False)
    agent_window.memory_type = "window"
    
    result = agent_window.run(
        message="Teste window memory",
        conversation_id="test_window"
    )
    print(f"✅ Window: {result['success']}")


def test_calculator_tool():
    """Teste 5: Ferramenta de cálculo"""
    print("\n" + "="*70)
    print("🧪 TESTE 5: Ferramenta Calculadora")
    print("="*70)
    
    agent = create_crypto_agent(verbose=True)
    
    result = agent.run(
        message="Quanto é 15% de 2500?",
        conversation_id="test_calc"
    )
    
    print(f"\n✅ Resposta: {result['response']}")


def test_conversation_management():
    """Teste 6: Gestão de conversas"""
    print("\n" + "="*70)
    print("🧪 TESTE 6: Gestão de Conversas")
    print("="*70)
    
    agent = create_crypto_agent(verbose=False)
    
    # Criar múltiplas conversas
    for i in range(3):
        agent.run(
            message=f"Conversa {i+1}",
            conversation_id=f"conv_{i+1}"
        )
    
    # Listar conversas
    conversations = memory_manager.list_conversations()
    print(f"\n📋 Conversas ativas: {conversations}")
    
    # Limpar uma conversa
    memory_manager.clear_conversation("conv_1")
    print(f"✅ Conversa 'conv_1' limpa")
    
    # Apagar uma conversa
    memory_manager.delete_conversation("conv_2")
    print(f"✅ Conversa 'conv_2' apagada")
    
    # Listar novamente
    conversations = memory_manager.list_conversations()
    print(f"📋 Conversas restantes: {conversations}")


def test_llm_config():
    """Teste 7: Configuração de LLM"""
    print("\n" + "="*70)
    print("🧪 TESTE 7: Configuração LLM")
    print("="*70)
    
    print(f"\n🔧 Configuração atual:")
    print(f"   • Tipo default: {llm_config.default_model}")
    print(f"   • Ollama URL: {llm_config.ollama_url}")
    print(f"   • OpenAI Key: {'✅ Configurada' if llm_config.openai_api_key else '❌ Não configurada'}")
    
    # Testar obtenção de LLM
    try:
        llm = llm_config.get_llm()
        print(f"\n✅ LLM carregado: {type(llm).__name__}")
    except Exception as e:
        print(f"\n❌ Erro ao carregar LLM: {str(e)}")


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("🚀 EXECUTAR TODOS OS TESTES DA FASE 1")
    print("="*70)
    
    try:
        test_llm_config()
        test_agent_basic()
        test_agent_with_tools()
        test_agent_with_memory()
        test_memory_types()
        test_calculator_tool()
        test_conversation_management()
        
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Escolhe qual teste executar
    import sys
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        test_func = globals().get(f"test_{test_name}")
        if test_func:
            test_func()
        else:
            print(f"Teste '{test_name}' não encontrado")
            print("\nTestes disponíveis:")
            print("  • agent_basic")
            print("  • agent_with_tools")
            print("  • agent_with_memory")
            print("  • memory_types")
            print("  • calculator_tool")
            print("  • conversation_management")
            print("  • llm_config")
    else:
        # Executar todos
        run_all_tests()
