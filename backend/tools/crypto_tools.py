# backend/tools/crypto_tools.py
"""
Ferramentas (Tools) que o agente pode usar
Nesta fase inicial, ferramentas simples de exemplo
"""
from typing import Optional
from langchain.tools import tool
from datetime import datetime


@tool
def get_current_time() -> str:
    """
    Retorna a data e hora atual.
    Útil quando o utilizador pergunta que horas são ou que dia é hoje.
    """
    now = datetime.now()
    return f"Data e hora atual: {now.strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def calculate_percentage(value: float, percentage: float) -> str:
    """
    Calcula uma percentagem de um valor.
    
    Args:
        value: Valor base
        percentage: Percentagem a calcular (ex: 10 para 10%)
    
    Exemplo: calculate_percentage(1000, 5) retorna 50
    """
    result = (value * percentage) / 100
    return f"{percentage}% de {value} é {result}"


@tool
def crypto_price_simulator(symbol: str, days: int = 7) -> str:
    """
    Simula dados de preço de criptomoeda (versão demo).
    Na Fase 2 vamos substituir por API real (CoinGecko).
    
    Args:
        symbol: Símbolo da cripto (ex: BTC, ETH)
        days: Número de dias para simular
    
    Retorna informação simulada de preço
    """
    # Preços demo - na Fase 2 isto será uma API real
    demo_prices = {
        "BTC": 45000,
        "ETH": 2800,
        "SOL": 110,
        "ADA": 0.55,
        "DOT": 8.2
    }
    
    base_price = demo_prices.get(symbol.upper(), 1000)
    
    return f"""
🪙 Dados de {symbol.upper()} (DEMO - últimos {days} dias):
   • Preço atual: ${base_price:,.2f}
   • Variação 24h: +2.5%
   • Mínima 7d: ${base_price * 0.92:,.2f}
   • Máxima 7d: ${base_price * 1.08:,.2f}
   
⚠️ Nota: Dados simulados. Na Fase 2 usaremos API real.
    """.strip()


@tool
def crypto_recommendation_simulator(risk_level: str = "medium") -> str:
    """
    Simula recomendações de investimento baseado em perfil de risco.
    
    Args:
        risk_level: Nível de risco ("low", "medium", "high")
    
    Retorna recomendações simuladas
    """
    recommendations = {
        "low": ["BTC (70%)", "ETH (20%)", "Stablecoins (10%)"],
        "medium": ["BTC (40%)", "ETH (30%)", "SOL (20%)", "ADA (10%)"],
        "high": ["Altcoins DeFi (40%)", "ETH (30%)", "SOL (20%)", "Memecoins (10%)"]
    }
    
    portfolio = recommendations.get(risk_level.lower(), recommendations["medium"])
    
    return f"""
📊 Portfólio Sugerido - Risco {risk_level.upper()}:
{chr(10).join(f'   • {coin}' for coin in portfolio)}

⚠️ Simulação educacional. Não é conselho financeiro.
    """.strip()


# Lista de todas as ferramentas disponíveis
AVAILABLE_TOOLS = [
    get_current_time,
    calculate_percentage,
    crypto_price_simulator,
    crypto_recommendation_simulator
]


def get_all_tools():
    """
    Retorna lista de todas as ferramentas disponíveis
    
    Uso:
        from tools.crypto_tools import get_all_tools
        tools = get_all_tools()
    """
    return AVAILABLE_TOOLS
